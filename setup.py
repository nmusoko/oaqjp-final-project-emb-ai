from setuptools import setup, find_packages

setup(
    name="EmotionDetection",
    version="0.1.0",
    description="Emotion detection helper using Watson NLP (Skills Network endpoint)",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
)
