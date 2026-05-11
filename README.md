# AI Interview Coach

A multi-agent AI system designed to help candidates prepare for job interviews through mock interviews, real-time feedback, and personalized coaching.

## Overview

The AI Interview Coach uses a sophisticated three-agent architecture to provide comprehensive interview preparation:

1. **Job Strategist**: Analyzes job descriptions and resumes to identify core competencies and predict relevant interview questions
2. **Interviewer**: Conducts realistic mock interviews while maintaining professional character
3. **Feedback Coach**: Provides detailed analysis of responses using the STAR method and competency alignment

## Features

- **Intelligent Question Prediction**: Analyzes job requirements to predict likely interview questions
- **STAR Method Evaluation**: Assesses responses for Situation, Task, Action, and Result structure
- **Real-time Feedback**: Provides immediate feedback on answer quality and competency alignment
- **Personalized Coaching**: Offers specific improvement suggestions based on your responses
- **Final Performance Summary**: Comprehensive analysis of your overall interview performance
- **Dual AI Support**: Works with either Google Gemini or OpenAI API

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd interview-coach
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env .env.local
# Add your AI API key to .env.local
```

### API Configuration

Choose one of the following:

**For Google Gemini (Recommended):**
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro-latest
```

**For OpenAI (Alternative):**
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

## Usage

Run the interview coach:
```bash
python -m interview_coach
```

Follow the prompts to:
1. Paste the job description you're interviewing for
2. Share your resume/CV
3. Engage in the mock interview
4. Receive detailed feedback

## Commands During Interview

- Type your answers normally to respond to questions
- Type `feedback` to see interim analysis of your responses
- Type `quit` to exit the interview early

## Architecture

The system follows a multi-agent pattern:

```
[Job Strategist] → Generates interview strategy
       ↓
[Interviewer] ←→ Conducts mock interview with user
       ↑
[Feedback Coach] → Evaluates responses in background
```

### Agent Details

#### Job Strategist
- Extracts technical and behavioral skills from job descriptions
- Predicts relevant interview questions based on job requirements
- Identifies core competencies to focus on

#### Interviewer
- Conducts realistic mock interviews
- Maintains professional character throughout
- Adapts questions based on user responses
- Provides subtle follow-ups for clarification

#### Feedback Coach
- Evaluates responses using STAR methodology
- Assesses clarity, conciseness, and competency alignment
- Provides constructive feedback and improvement suggestions
- Generates comprehensive performance summaries
## Technologies Used

- Python 3.12+
- Google Gemini API (or OpenAI API as fallback)
- Rich (for enhanced terminal output)
- Modular agent architecture

## Customization

The system is designed to be easily customizable:

- Modify agent prompts in their respective files
- Extend evaluation criteria in the Feedback Coach
- Add new question templates to the Job Strategist
- Customize feedback generation logic

## Troubleshooting

If you encounter issues:
1. Verify your API key is correctly set in the .env file
2. Check that you have internet connectivity
3. Ensure you have the required dependencies installed
4. Confirm your API provider has sufficient quota

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Support

If you have questions or need assistance:
- Check the documentation
- Open an issue in the repository
- Review the example configurations
