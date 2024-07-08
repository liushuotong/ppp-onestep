import re
import csv
import sys
import subprocess
import argparse

# dict to store the hydrophobicity scores
hydrophobicity_scores = {
    'A': 1.800, 'R': -4.500, 'N': -3.500, 'D': -3.500,
    'C': 2.500, 'Q': -3.500, 'E': -3.500, 'G': -0.400,
    'H': -3.200, 'I': 4.500, 'L': 3.800, 'K': -3.900,
    'M': 1.900, 'F': 2.800, 'P': -1.600, 'S': -0.800,
    'T': -0.700, 'W': -0.900, 'Y': -1.300, 'V': 4.200
}


# regex pattern to extract the desired information from EMBOSS
pattern = r"""PEPSTATS of (\S+) from (\S+) to (\S+)(\s+)Molecular weight = (\S+)(\s+)Residues = (\S+)(\s+)Average Residue Weight  = (\S+)(\s+)Charge   = (\S+)(\s+)Isoelectric Point = (\S+)(\s+)A280 Molar Extinction Coefficients  = (\S+) (\S+)   (\S+) (\S+) (\S+)(\s+)A280 Extinction Coefficients 1mg/ml = (\S+) (\S+)   (\S+) (\S+) (\S+)(\s+)(?:Improbability|Probability) of expression in inclusion bodies = (\S+)(\s+)Residue		Number		Mole%		DayhoffStat(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+) = (\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)"""

def predict_protein_properties(sequence_file, output_PATH):
    """
    Predicts protein properties based on the input sequence file and saves the EMBOSS pepstats output to the specified output file.
    
    Parameters:
    sequence_file (str): Path to the input sequence file.
    output_file (str): Path to the output file where the EMBOSS pepstats output will be saved.
    """
    emboss_command = ['pepstats', sequence_file, output_PATH + '/protein_properties.txt']
    try:
        subprocess.run(emboss_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing EMBOSS pepstats: {e}")

def main(sequence_file, output_PATH):
    """
    Predicts protein properties based on the input sequence file and saves the EMBOSS pepstats output to the specified output file.

    Parameters:
    sequence_file (str): Path to the input sequence file.
    output_file (str): Path to the output file where the EMBOSS pepstats output will be saved.
    """
    predict_protein_properties(sequence_file, output_PATH)
    with open(output_PATH + '/protein_properties.txt', 'r') as file:
        text = file.read()
    matches = re.finditer(pattern, text, flags=0)
    if not matches:
        print("No matches found.")
    output_tsv = output_PATH + '/ppp-onestep_output.tsv'
    with open(output_tsv, "w", newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(["Sequence",
                         "Molecular Weight",
                         "Residues",
                         "Average Residue Weight",
                         "Charge",
                         "Isoelectric Point",
                         "Hydrophobicity Scores"])
    for match in matches:
        sequence_name = match[1]
        start_position = match[2]
        end_position = match[3]
        molecular_weight = match[5]
        residues = match[7]
        avg_residue_weight = match[9]
        charge = match[11]
        isoelectric_point = match[13]
        hy_scores_all = hydrophobicity_scores['A']*int(match[33]) + \
            hydrophobicity_scores['R']*int(match[186]) + \
            hydrophobicity_scores['N']*int(match[150]) + \
            hydrophobicity_scores['D']*int(match[60]) + \
            hydrophobicity_scores['C']*int(match[51]) + \
            hydrophobicity_scores['Q']*int(match[177]) + \
            hydrophobicity_scores['E']*int(match[69]) + \
            hydrophobicity_scores['G']*int(match[87]) + \
            hydrophobicity_scores['H']*int(match[96]) + \
            hydrophobicity_scores['I']*int(match[105]) + \
            hydrophobicity_scores['L']*int(match[132]) + \
            hydrophobicity_scores['K']*int(match[123]) + \
            hydrophobicity_scores['M']*int(match[141]) + \
            hydrophobicity_scores['F']*int(match[78]) + \
            hydrophobicity_scores['P']*int(match[168]) + \
            hydrophobicity_scores['S']*int(match[195]) + \
            hydrophobicity_scores['T']*int(match[204]) + \
            hydrophobicity_scores['W']*int(match[231]) + \
            hydrophobicity_scores['Y']*int(match[249]) + \
            hydrophobicity_scores['V']*int(match[222])
        hy_scores = hy_scores_all/float(match[3])
        with open(output_tsv, "a", newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow([sequence_name, molecular_weight, residues, avg_residue_weight, charge, isoelectric_point, hy_scores])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict protein properties.')
    parser.add_argument('-f', '--fasta', required=True, help='Protein sequence file')
    parser.add_argument('-o', '--out', required=True, help='Output PATH')
    args = parser.parse_args()
    protein_sequence_file = args.fasta
    output_PATH = args.out
    main(protein_sequence_file, output_PATH)
    print("ppp-onestep result saved to " + output_PATH + '/ppp-onestep_output.tsv')