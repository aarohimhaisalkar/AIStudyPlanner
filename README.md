# 📚 AI Study Planner

An intelligent, AI-powered web application that helps students generate personalized study plans based on their available time, subjects, and deadlines. Built with Python, Streamlit, and OpenAI API.

## 🎯 Features

### 🤖 AI-Powered Planning
- **Personalized Study Schedules**: Generate custom study plans using advanced AI algorithms
- **Smart Task Distribution**: Automatically allocate study time across subjects
- **Adaptive Recommendations**: Get intelligent study tips and optimization suggestions
- **Flexible Scheduling**: Choose your preferred study times and break patterns

### 📊 Comprehensive Analytics
- **Visual Progress Tracking**: Interactive charts showing study progress and completion rates
- **Subject Performance Analysis**: Track performance across different subjects
- **Study Time Distribution**: See how your time is allocated across activities
- **Goal Progress Monitoring**: Visual gauges showing progress towards study goals

### 📈 Progress Management
- **Task Completion Tracking**: Mark tasks as completed and monitor progress
- **Study Streaks**: Keep track of consecutive study days
- **Milestone Tracking**: Set and achieve study milestones
- **Performance Insights**: Get personalized recommendations based on your progress

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Comfortable studying in any lighting condition
- **Interactive Charts**: Beautiful, interactive visualizations using Plotly
- **Intuitive Navigation**: Easy-to-use sidebar navigation with clear sections

### 💾 Data Management
- **Export Functionality**: Download your study plans as CSV files
- **Progress Backup**: Automatic backup of your study data
- **Session Persistence**: Your progress is saved between sessions
- **Data Analytics**: Comprehensive statistics about your study habits

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: OpenAI GPT-3.5 Turbo
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Altair
- **Styling**: Custom CSS with responsive design
- **Backend**: Python 3.8+

## 📦 Project Structure

```
AIStudyPlanner/
│
├── app.py                 # Main Streamlit application
├── planner.py             # AI study plan generator
├── analytics.py           # Data visualization and analytics
├── utils.py               # Utility functions and helpers
├── styles.css             # Custom CSS styling
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── user_data.json        # User data storage (auto-generated)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (optional, for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AIStudyPlanner.git
   cd AIStudyPlanner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Or set it as an environment variable:
   ```bash
   # Windows
   set OPENAI_API_KEY=your_openai_api_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Generate Your First Study Plan

1. Navigate to **"Generate Study Plan"** in the sidebar
2. Fill in your study details:
   - **Subjects**: Enter each subject on a new line
   - **Daily Study Hours**: Choose how many hours you can study per day
   - **Exam Date**: Select your exam or deadline date
   - **Priority Level**: Choose how important this exam is
   - **Difficulty Level**: Select the difficulty of your subjects
   - **Study Preference**: Choose your preferred study time
3. Click **"Generate Study Plan"** and wait for the AI to create your personalized schedule

### 2. Track Your Progress

1. Go to **"Dashboard"** to see your daily schedule
2. Check off completed tasks using the checkboxes
3. Monitor your progress in the **"Progress Tracker"**
4. View detailed analytics in the **"Analytics"** section

### 3. Analyze Your Performance

1. Visit the **"Analytics"** page to see:
   - Study time distribution across subjects
   - Completion rates and progress trends
   - Study intensity heatmaps
   - Goal tracking visualizations

### 4. Export and Backup

1. Download your study plan as CSV from the Dashboard
2. Your progress is automatically saved
3. Data is stored locally in `user_data.json`

## 🎨 Customization

### Adding New Features

The modular structure makes it easy to add new features:

1. **New Analytics**: Add functions to `analytics.py`
2. **AI Features**: Extend `planner.py` with new AI capabilities
3. **Utility Functions**: Add helpers to `utils.py`
4. **UI Components**: Modify `app.py` for new interface elements

### Styling Changes

Edit `styles.css` to customize:
- Color schemes
- Layout styles
- Responsive breakpoints
- Dark mode support
- Animations and transitions

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Streamlit Configuration

Create a `.streamlit/config.toml` file for advanced configuration:

```toml
[server]
port = 8501
address = "localhost"
headless = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2c3e50"
```

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Set your OpenAI API key in the deployment settings
4. Deploy!

### Other Platforms

The application can be deployed on:
- **Heroku**: Using the Streamlit buildpack
- **Railway**: Simple deployment with environment variables
- **DigitalOcean App Platform**: Container-based deployment
- **AWS/GCP**: Deploy as a containerized application

## 📱 Mobile Support

The application is fully responsive and works on:
- **iOS Safari**: Full functionality on iPhones and iPads
- **Android Chrome**: Complete support on Android devices
- **Tablets**: Optimized layout for iPad and Android tablets

## 🔒 Privacy & Security

- **Local Data Storage**: All user data is stored locally
- **No Data Collection**: The app doesn't collect personal information
- **API Security**: OpenAI API calls are made directly from your session
- **Session Privacy**: Data is not shared between users

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature description'`
5. Push to the branch: `git push origin feature-name`
6. Create a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Add comments to explain complex logic
- Test new features thoroughly
- Update documentation as needed
- Use meaningful variable and function names

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Error**
```
Error: OpenAI API key not found
```
**Solution**: Make sure your OpenAI API key is set correctly in the `.env` file or as an environment variable.

**Module Not Found**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Activate your virtual environment and install dependencies: `pip install -r requirements.txt`

**Port Already in Use**
```
Port 8501 is already in use
```
**Solution**: Either stop the other process or run on a different port: `streamlit run app.py --server.port 8502`

### Getting Help

1. Check the [Issues](https://github.com/yourusername/AIStudyPlanner/issues) page
2. Search existing issues for similar problems
3. Create a new issue with detailed information
4. Include error messages and steps to reproduce

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the powerful GPT API
- **Streamlit** for the amazing web framework
- **Plotly** for beautiful data visualizations
- The open-source community for inspiration and tools

## 📞 Support

If you need help or have questions:

- 📧 Email: your-email@example.com
- 💬 Discord: [Join our community](https://discord.gg/your-server)
- 🐛 Issues: [Report on GitHub](https://github.com/yourusername/AIStudyPlanner/issues)
- 📖 Documentation: [View full docs](https://yourusername.github.io/AIStudyPlanner)

## 🌟 Star History

If this project helped you, consider giving it a star! ⭐

---

**Made with ❤️ by AI Study Planner Team**

*"Empowering students to achieve their academic goals through intelligent planning"*
