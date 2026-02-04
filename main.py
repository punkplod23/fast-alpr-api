from fast_alpr import ALPR
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import base64
from typing import Dict, Any

mcp = FastMCP()
mcp_app = mcp.http_app(path="/")
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app)  # MCP endpoint at /mcp

alpr = ALPR(
            detector_model="yolo-v9-t-384-license-plate-end2end",
            ocr_model="cct-xs-v1-global-model",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# --- Pydantic Model ---
class Base64Image(BaseModel):
    # The client sends the Base64 string in this field
    image_base64: str = Field(..., description="Base64 encoded image data.")

# --- Endpoint to Process Base64 Image In-Memory ---
@app.post("/process-base64-image/")
async def process_base64_image(data: Base64Image) -> Dict[str, Any]:
    try:
        # 1. Strip the data URI prefix if it exists (e.g., "data:image/png;base64,")
        encoded_data = data.image_base64
        mime_type = "unknown"
        
        if ',' in encoded_data:
            # Assuming the format is 'data:MIME_TYPE;base64,ACTUAL_DATA'
            header, encoded_data = encoded_data.split(',', 1)
            # Simple attempt to extract MIME type from the header
            if ':' in header and ';' in header:
                mime_type = header.split(':')[1].split(';')[0]
        
        # 2. Decode the Base64 string to raw image bytes
        image_bytes = base64.b64decode(encoded_data)
        
        # 3. Perform in-memory processing here (e.g., image analysis, machine learning inference)
        # ⚠️ At this point, 'image_bytes' is the actual binary data of the image. 
        # You could use libraries like PIL/Pillow or OpenCV to work with it:
        # 
        # from PIL import Image
        # from io import BytesIO
        # image = Image.open(BytesIO(image_bytes))
        # # image.resize(...) or image.convert(...)
        


        # Convert image bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        alpr_results = alpr.predict(image)
        

        # 4. Return the response with ALPR results
        return {
            "message": "Base64 image successfully processed (in-memory).",
            "size_bytes": len(image_bytes),
            "inferred_mime_type": mime_type,
            "alpr_results": alpr_results
        }
        
    except base64.binascii.Error:
        # This handles cases where the Base64 string is improperly formatted or padded
        raise HTTPException(
            status_code=422, detail="Invalid Base64 string. Check padding or characters."
        )
    except Exception as e:
        # Catch other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An error occurred during processing: {e}"
        )

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    alpr_results = alpr.predict(image)
    return alpr_results

@mcp.tool()
def detect_license_plate(image_base64: str) -> Dict[str, Any]:
    """Detect license plate from a Base64 encoded image."""
    try:
        image_bytes = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        decoded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        alpr_results = alpr.predict(decoded_image)
        return {"results": alpr_results}
    except Exception as e:
        return {"error": str(e)}