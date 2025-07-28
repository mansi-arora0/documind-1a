# Use AMD64-compatible lightweight Python image
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Copy script into container
COPY process_pdfs.py .

# Install only the required packages (no internet calls)
RUN pip install --no-cache-dir pdfminer.six

# Entry point to run processing script
CMD ["python", "process_pdfs.py"]

