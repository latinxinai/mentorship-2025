"""
Certificate Generator for LatinX in AI Mentorship Program
Generates PDF certificates for mentors who participated in the program
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import pandas as pd
from pathlib import Path
from datetime import datetime

# Program details
PROGRAM_NAME = "LatinX in AI Mentorship Program"
START_DATE = "September 20th"
END_DATE = "December 1st"
YEAR = "2025"

def load_mentor_data(csv_file):
    """Load mentor data from CSV and remove duplicates"""
    df = pd.read_csv(csv_file)
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Remove duplicates based on email
    df_unique = df.drop_duplicates(subset=['Email'], keep='first')
    
    print(f"Total mentors (with duplicates): {len(df)}")
    print(f"Unique mentors: {len(df_unique)}")
    
    return df_unique

def create_certificate(mentor_data, output_dir, logo_path=None, signature_path=None):
    """
    Create a certificate for a mentor
    
    Args:
        mentor_data: Dictionary with 'First Name', 'Last Name', 'Email'
        output_dir: Directory to save the certificate
        logo_path: Path to the LXAI logo image (optional)
        signature_path: Path to the signature image (optional)
    """
    first_name = mentor_data['First Name'].strip()
    last_name = mentor_data['Last Name'].strip()
    full_name = f"{first_name} {last_name}"
    
    # Create safe filename
    safe_name = f"{first_name}_{last_name}".replace(" ", "_")
    output_path = output_dir / f"Certificate_{safe_name}.pdf"
    
    # Create PDF in landscape orientation
    c = canvas.Canvas(str(output_path), pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Colors
    lxai_color = HexColor('#000000')  # Black
    text_color = HexColor('#333333')  # Dark gray
    accent_color = HexColor('#FF6B35')  # Orange accent
    
    # Draw border
    c.setStrokeColor(lxai_color)
    c.setLineWidth(3)
    c.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch)
    
    # Add decorative inner border
    c.setStrokeColor(accent_color)
    c.setLineWidth(1)
    c.rect(0.6*inch, 0.6*inch, width-1.2*inch, height-1.2*inch)
    
    # Add logo if provided
    if logo_path and Path(logo_path).exists():
        try:
            c.drawImage(logo_path, width/2 - 1.5*inch, height - 2*inch, 
                       width=3*inch, height=1*inch, preserveAspectRatio=True, 
                       mask='auto')
        except Exception as e:
            print(f"Warning: Could not add logo - {e}")
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(lxai_color)
    title_y = height - 2.8*inch if logo_path else height - 1.5*inch
    c.drawCentredString(width/2, title_y, "CERTIFICATE OF APPRECIATION")
    
    # Subtitle
    c.setFont("Helvetica", 14)
    c.setFillColor(text_color)
    c.drawCentredString(width/2, title_y - 0.4*inch, "This certificate is proudly presented to")
    
    # Mentor name (larger and bold)
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(lxai_color)
    c.drawCentredString(width/2, title_y - 1.2*inch, full_name)
    
    # Draw decorative line under name
    c.setStrokeColor(accent_color)
    c.setLineWidth(2)
    name_width = c.stringWidth(full_name, "Helvetica-Bold", 36)
    c.line(width/2 - name_width/2 - 0.3*inch, title_y - 1.35*inch,
           width/2 + name_width/2 + 0.3*inch, title_y - 1.35*inch)
    
    # Recognition text
    c.setFont("Helvetica", 14)
    c.setFillColor(text_color)
    
    recognition_text = [
        "For their outstanding contribution as a Mentor in the",
        f"{PROGRAM_NAME}",
        f"held from {START_DATE} to {END_DATE}, {YEAR}",
        "",
        "Your dedication to fostering diversity and supporting the next generation",
        "of AI researchers and practitioners is deeply appreciated."
    ]
    
    text_y = title_y - 2.0*inch
    for line in recognition_text:
        if "LatinX in AI" in line:
            c.setFont("Helvetica-Bold", 15)
            c.setFillColor(lxai_color)
        else:
            c.setFont("Helvetica", 14)
            c.setFillColor(text_color)
        c.drawCentredString(width/2, text_y, line)
        text_y -= 0.3*inch
    
    # Signature section
    signature_y = 1.5*inch
    
    # Add signature image if provided
    if signature_path and Path(signature_path).exists():
        try:
            # Place signature image above the line (centered)
            sig_width = 3*inch  # Adjust size as needed
            sig_height = 1.8*inch  # Adjust size as needed
            c.drawImage(signature_path, 
                       width/2 - sig_width/2, 
                       signature_y - inch + 20,  # Slightly above the line
                       width=sig_width, 
                       height=sig_height, 
                       preserveAspectRatio=True, 
                       mask='auto')
        except Exception as e:
            print(f"Warning: Could not add signature image - {e}")
    
    # Centered signature line
    c.setStrokeColor(text_color)
    c.setLineWidth(1)
    signature_line_width = 3*inch
    c.line(width/2 - signature_line_width/2, signature_y, 
           width/2 + signature_line_width/2, signature_y)
    
    # Name and title
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(text_color)
    c.drawCentredString(width/2, signature_y - 0.25*inch, "Felipe A. Lopes")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, signature_y - 0.45*inch, "Mentorship Program Chair")
    
    # Date
    
    # Save PDF
    c.save()
    print(f"✓ Generated certificate for {full_name}")
    return output_path

def main():
    """Main function to generate all certificates"""
    # Setup
    csv_file = "/mnt/user-data/uploads/mentors.csv"  # Adjust path as needed
    output_dir = Path("./outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logo_path = "./lxai-logo.webp"
    
    # ADD YOUR SIGNATURE IMAGE PATH HERE
    # For example: signature_path = "/mnt/user-data/uploads/signature.png"
    signature_path = None  # Set this to your signature image path
    
    # Check if signature file exists in uploads
    possible_signature_files = [
        "./signature.png"
    ]
    
    for sig_file in possible_signature_files:
        if Path(sig_file).exists():
            signature_path = sig_file
            print(f"Found signature file: {signature_path}")
            break
    
    print("="*60)
    print("LatinX in AI Mentorship Program - Certificate Generator")
    print("="*60)
    print()
    
    # Load mentor data
    print("Loading mentor data...")
    
    # Create DataFrame from the provided data
    mentors_data = {
        'First Name': ['Akshata Kishore', 'Bodhisatta', 'Brian K. S.', 
                       'Emmanuel', 'Felipe', 'Heitor', 'Karls', 
                       'Salvador', 'Santiago', 'Sergio', 'Shagun', 'Silmara'],
        'Last Name': ['Moharir', 'Maiti', 'Isaac Medina', 
                      'Ovalle Magallanes', 'Moreno', 'Medeiros', 'Caballero Barajas', 
                      'Hinojosa', 'Hincapie Potes', 'Calvo Ordoñez', 'Sodhani', 
                      'Furtado da Silva'],
        'Email': ['akshatankishore5@gmail.com', 'bodhisattamaiti2022@u.northwestern.edu',
                  'brian.isaac-medina@openworksengineering.com',
                  'eovalle@lasallebajio.edu.mx', 'felipe.moreno.vera@gmail.com', 
                  'hrm@cin.ufpe.br', 'klcaballero@gmail.com',
                  'salvador.hinojosa@tec.mx', 'shpotes3@gmail.com',
                  'sergio.calvoordonez@maths.ox.ac.uk', 'sshagunsodhani@gmail.com',
                  'silmara.furtado@yahoo.com.br']
    }
    
    df = pd.DataFrame(mentors_data)
    
    print(f"Found {len(df)} unique mentors")
    print()
    
    # Generate certificates
    print("Generating certificates...")
    print()
    
    generated_count = 0
    for idx, row in df.iterrows():
        try:
            create_certificate(row.to_dict(), output_dir, logo_path, signature_path)
            generated_count += 1
        except Exception as e:
            print(f"✗ Error generating certificate for {row['First Name']} {row['Last Name']}: {e}")
    
    print()
    print("="*60)
    print(f"Certificate generation complete!")
    print(f"Generated {generated_count} certificates")
    print(f"Output directory: {output_dir}")
    print("="*60)

if __name__ == "__main__":
    main()