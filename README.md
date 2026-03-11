# 📚 AI Study Planner

A responsive, intelligent study planning application built with Streamlit that helps students create personalized study schedules using AI-powered recommendations.

## 🌟 Features

### 📱 Responsive Design
- **Mobile-first design** that works seamlessly on desktop, tablet, and mobile
- **Collapsible sidebar** for smaller screens
- **Adaptive layouts** using Streamlit columns and CSS media queries
- **Touch-friendly** interface elements

### 📝 Smart Study Plan Generation
- **Intelligent topic distribution** based on difficulty level
- **Automated scheduling** that considers exam dates and available study time
- **Personalized study tips** tailored to subject and difficulty
- **Flexible planning** for various subjects (Mathematics, Physics, Chemistry, Biology, Computer Science, History, Literature)

### 📊 Progress Tracking & Analytics
- **Real-time progress monitoring** with visual indicators
- **Interactive charts** showing daily workload distribution
- **Completion statistics** with percentage-based tracking
- **Study streak counter** for motivation

### 🤖 AI-Powered Features (Optional)
- **Personalized study recommendations** using OpenAI API
- **Motivational messages** based on progress
- **Smart break suggestions** for optimal learning
- **Weekly study summaries** with AI insights

### 💾 Export Functionality
- **CSV export** for study plans and progress data
- **Excel export** with multiple sheets (Summary, Daily Plan, Study Tips)
- **Downloadable reports** for offline reference

### 🎨 User Experience
- **Dark mode toggle** for comfortable studying
- **Motivational quotes** to keep students inspired
- **Interactive checkboxes** for marking completed topics
- **Clean, modern UI** with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** the project files to your local machine

2. **Navigate to the project directory:**
   ```bash
   cd AIStudyPlanner
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Optional: AI Features Setup

To enable AI-powered features, you'll need an OpenAI API key:

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/)

2. **Set the API key** as an environment variable:
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY=your_api_key_here
   ```

3. **Install the OpenAI package:**
   ```bash
   pip install openai
   ```

4. **Uncomment the openai line** in `requirements.txt` and reinstall

## 📖 Usage Guide

### Creating a Study Plan

1. **Fill in the study plan form:**
   - **Subject Name**: Enter the subject you're studying
   - **Total Topics**: Number of topics to cover (1-100)
   - **Exam Date**: Your target exam date
   - **Hours Per Day**: Available study hours (1-12)
   - **Difficulty Level**: Easy, Medium, or Hard

2. **Click "Generate Study Plan"** to create your personalized schedule

### Tracking Progress

1. **View your daily schedule** with expandable sections
2. **Check off completed topics** using the checkboxes
3. **Monitor your progress** with the progress bar and metrics
4. **View visual analytics** in the charts section

### Exporting Your Plan

1. **Choose your export format**: CSV or Excel
2. **Click the download button** to save your study plan
3. **Use the exported file** for offline reference or sharing

### Using AI Features

If AI is enabled, you'll receive:
- **Personalized study tips** based on your learning preferences
- **Motivational messages** that adapt to your progress
- **Smart break recommendations** for optimal study sessions

## 🏗️ Project Structure

```
AI-Study-Planner/
│
├── app.py              # Main Streamlit application
├── planner.py          # Study plan generation logic
├── ai_helper.py        # OpenAI integration (optional)
├── utils.py            # Utility functions and helpers
├── styles.css          # Responsive CSS styles
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

### File Descriptions

- **`app.py`**: Main application with UI components, form handling, and session state management
- **`planner.py`**: Core study planning logic with intelligent topic distribution algorithms
- **`ai_helper.py`**: Optional AI integration for personalized recommendations
- **`utils.py`**: Helper functions for validation, exports, styling, and calculations
- **`styles.css`**: Comprehensive responsive CSS with mobile-first design
- **`requirements.txt`**: Python package dependencies

## 🎯 Key Features Explained

### Smart Topic Distribution

The planner intelligently distributes topics across available study days:

- **Easy Difficulty**: 1.2x multiplier (more topics per day)
- **Medium Difficulty**: 1.0x multiplier (balanced distribution)
- **Hard Difficulty**: 0.8x multiplier (fewer topics per day for deeper learning)

### Progress Tracking System

- **Real-time updates** as you check off topics
- **Visual progress indicators** with percentage completion
- **Study streak counter** that increases every 3 completed topics
- **Status messages** that adapt to your progress level

### Responsive Design

The application adapts seamlessly to different screen sizes:

- **Mobile (< 480px)**: Single column layout, full-width buttons, larger touch targets
- **Tablet (481px - 768px)**: Two-column layout, optimized spacing
- **Desktop (> 768px)**: Multi-column layout with maximum functionality

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Create a GitHub repository** with your project files

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**

3. **Connect your GitHub account** and select the repository

4. **Configure the deployment:**
   - Main file path: `app.py`
   - Python version: 3.9 or higher
   - Add environment variables (if using AI features)

5. **Deploy** and share your app with others!

### Environment Variables for Deployment

If using AI features, add these environment variables in Streamlit Cloud:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🔧 Customization

### Adding New Subjects

To add new subject templates, edit the `topic_templates` dictionary in `planner.py`:

```python
self.topic_templates["Your Subject"] = [
    "Topic 1", "Topic 2", "Topic 3", "Topic 4"
]
```

### Modifying Difficulty Levels

Adjust the difficulty multipliers in `planner.py`:

```python
self.difficulty_multipliers = {
    "Easy": 1.2,      # 20% more topics per day
    "Medium": 1.0,    # Normal distribution
    "Hard": 0.8       # 20% fewer topics for deeper study
}
```

### Custom Styling

Modify `styles.css` to customize:
- Colors and themes
- Layout and spacing
- Animations and transitions
- Mobile responsiveness

## 🐛 Troubleshooting

### Common Issues

1. **App won't start**: Check that all dependencies are installed correctly
2. **AI features not working**: Verify your OpenAI API key is set correctly
3. **Mobile layout issues**: Clear browser cache and refresh
4. **Export not working**: Ensure `openpyxl` is installed for Excel export

### Getting Help

- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Review the [OpenAI API documentation](https://platform.openai.com/docs)
- Create an issue in your project repository for specific problems

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add feature description'`
5. **Push to the branch**: `git push origin feature-name`
6. **Open a pull request**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualizations
- **OpenAI** for AI-powered features
- The study community for feedback and inspiration

## 📞 Support

If you encounter any issues or have questions:

1. **Check this README** for troubleshooting tips
2. **Review the code comments** for detailed explanations
3. **Create an issue** in your project repository
4. **Reach out to the Streamlit community** for support

---

**Happy Studying! 📚✨**

Made with ❤️ using Streamlit
