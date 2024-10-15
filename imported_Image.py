from write_to_new_image import ConvertToSingleImage 
def dBaseImage():
    """Function to extract the combined image from the database."""
    converter = ConvertToSingleImage()  
    imgDatabase = converter.loadDatabase() 
    return imgDatabase

