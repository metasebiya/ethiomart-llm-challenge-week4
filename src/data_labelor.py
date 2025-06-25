def interactive_conll_labeler():
    """
    An interactive script to help label text data in CoNLL format.
    """
    # --- Configuration ---
    input_file = 'scraped_messages.txt'  # Your raw text file
    output_file = 'labeled_data.conll'  # The file where labeled data will be saved

    # Define the entities you want to label
    labels = {
        '1': 'O',  # Outside
        '2': 'B-Product',  # Beginning of a Product
        '3': 'I-Product',  # Inside a Product
        '4': 'B-LOC',  # Beginning of a Location
        '5': 'I-LOC',  # Inside a Location
        '6': 'B-PRICE',  # Beginning of a Price
        '7': 'I-PRICE',  # Inside a Price
    }

    # --- Read Input File ---
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        print("Please create it and add your scraped messages, one per line.")
        return

    print("--- Starting Interactive Labeling Session ---")
    print(f"Messages will be read from: {input_file}")
    print(f"Labeled data will be saved to: {output_file}\n")

    # --- Main Labeling Loop ---
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for i, message in enumerate(messages):
            print(f"\n--- Labeling Message {i + 1}/{len(messages)} ---")
            print(f"MESSAGE: {message}")

            tokens = message.split()  # Simple whitespace tokenizer
            labeled_tokens = []

            for token in tokens:
                while True:  # Loop until valid input is received
                    print(f"\nTOKEN: '{token}'")
                    # Display label options
                    for key, value in labels.items():
                        print(f"  {key}: {value}")

                    choice = input(f"Enter label number for '{token}': ")

                    if choice in labels:
                        label = labels[choice]
                        labeled_tokens.append(f"{token} {label}\n")
                        break  # Exit the while loop for this token
                    else:
                        print("--- Invalid choice! Please enter a number from the list. ---")

            # Write the labeled message to the output file
            f_out.writelines(labeled_tokens)
            f_out.write("\n")  # Add a blank line to separate messages
            print(f"--- Message {i + 1} saved to {output_file} ---")

    print("\n\n--- Labeling Complete! ---")
    print(f"All labeled data has been saved to '{output_file}'.")


# Run the interactive labeler
interactive_conll_labeler()