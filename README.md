# Protein Properties Predictor

Protein Properties Predictor (ppp-onestep) is a Python script that predicts protein properties based on input sequence files. It utilizes the EMBOSS pepstats tool to generate the necessary data and calculates hydrophobicity scores for the protein sequences.

## Features

- Extracts various protein properties using EMBOSS pepstats
- Calculates hydrophobicity scores for each sequence
- Outputs results in a TSV file

## Requirements

- Python 3.x
- EMBOSS suite

## Installation

Ensure you have EMBOSS installed on your system. You can install it using the following commands:

### Debian/Ubuntu

```bash
sudo apt-get update
sudo apt-get install emboss
```

### Fedora

```bash
sudo dnf install emboss
```

### macOS (using Homebrew)

```bash
brew install emboss
```

Clone the repository:

```bash
git clone https://github.com/liushuotong/protein-properties-predictor.git
cd protein-properties-predictor
```

## Usage

Run the script using the following command:

```bash
python ppp-onestep.py -f <path_to_fasta_file> -o <output_directory>
```

**Tips:**

You don't need to add `\` after `-o` args' last word!

### Arguments

- `-f, --fasta`: Path to the input protein sequence file in FASTA format.
- `-o, --out`: Directory where the output files will be saved.

### Example

```bash
python ppp-onestep.py -f example.fasta -o results/
```

## Output

The script generates an output TSV file named `ppp-onestep_output.tsv` in the specified output directory. The TSV file contains the following columns:

- Sequence
- Molecular Weight
- Residues
- Average Residue Weight
- Charge
- Isoelectric Point
- Hydrophobicity Scores

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [EMBOSS](http://emboss.sourceforge.net/) for providing the pepstats tool.

---

liushuotong  SDUW  Shandong University
Email: liushuotong0218@gmail.com  

----

This `README.md` includes your personal details at the end. If you have any other specific changes or additions, let me know!
