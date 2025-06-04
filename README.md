# Palm Analysis Web Application

This web application combines traditional palmistry with modern computer vision techniques to provide personalized palm readings. The application analyzes palm images and incorporates zodiac signs and gender-based insights for a comprehensive analysis.

## Features

- Palm image analysis using computer vision
- Zodiac sign integration based on date of birth
- Gender-specific insights
- Interactive web interface
- Annotated palm image results
- Comprehensive personality and life path analysis

## Tech Stack

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV (via finger_analysis.py)
- **Frontend**: HTML, JavaScript
- **File Handling**: UUID-based unique file management

## Project Structure

```
├── app.py                 # Main Flask application
├── finger_analysis.py     # Palm analysis logic
├── standalone.py         # Standalone version of the application
├── comp.py              # Component analysis
├── templates/           # HTML templates
├── static/             # Static files and results
├── uploads/            # Temporary storage for uploaded images
└── images/            # Project images
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask opencv-python
   ```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```
2. Open a web browser and navigate to `http://localhost:5001`
3. Upload a palm image
4. Enter your date of birth and gender
5. Receive your personalized palm analysis with annotated results

## Features in Detail

### Palm Analysis
- Finger length and proportion analysis
- Palm line detection and interpretation
- Personality trait correlation

### Zodiac Integration
- Automatic zodiac sign calculation based on birth date
- Personalized zodiac insights
- Combined analysis with palm reading

### Gender-Based Insights
- Customized interpretations based on gender
- Unique personality trait analysis
- Tailored life path guidance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for open use and modification. Please provide attribution when using or adapting this code.

## References

The project incorporates knowledge from various palmistry sources:
- Palmistry For All Western Techniques
- Amazing Palmistry Secrets Western Techniques
- Practical Palmistry Hindu techniques 
