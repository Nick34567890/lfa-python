import sys
from Tokenizer import Tokenizer  # Assuming you have this in your project structure

def main():
    # Example input string (you can load this from a file if necessary)
    input_text = """
    BATCH #rawImages = "C:/raw/";
    FOREACH IMG $img IN #rawImages {
        INT $width = METADATA $img FWIDTH;
        INT $height = METADATA $img FHEIGHT;
        
        CROP $img (1920, 1080);
        
        DOUBLE $fileSize = METADATA $img FSIZE;
        IF $fileSize > 10000 {
            SET $img NEGATIVE;
        }
        ELSE {
            SET $img SEPIA;
        }
        
        IF $height > $width {
            ROTATE $img RIGHT;
        }
    }
    """

    # Initialize the tokenizer with the input text
    tokenizer = Tokenizer(input_text)
    tokens = tokenizer.tokenize()

    # Print out all the tokens
    print("Tokens:")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
