import statistics


def analyze_scores(scores):
    total_score = sum(scores)
    max_score = max(scores)
    min_score = min(scores)
    average_score = statistics.mean(scores)
    median_score = statistics.median(scores)

    return {
        'total': total_score,
        'max': max_score,
        'min': min_score,
        'average': average_score,
        'median': median_score
    }


def print_analysis(analysis):
    print(f"Total Score: {analysis['total']}")
    print(f"Highest Score: {analysis['max']}")
    print(f"Lowest Score: {analysis['min']}")
    print(f"Average Score: {analysis['average']:.2f}")
    print(f"Median Score: {analysis['median']}")


def find_outliers(scores, analysis):
    lower_bound = analysis['average'] - 2 * statistics.stdev(scores)
    upper_bound = analysis['average'] + 2 * statistics.stdev(scores)
    outliers = [score for score in scores if score < lower_bound or score > upper_bound]
    return outliers


student_scores = [150, 142, 185, 120, 171, 184, 149, 24, 59, 68, 199, 78, 65, 89, 86, 55, 91, 64, 89]

analysis_results = analyze_scores(student_scores)
print_analysis(analysis_results)

outliers = find_outliers(student_scores, analysis_results)
print(f"\nOutlier scores: {outliers}")

# Bonus: Visualisierung
import matplotlib.pyplot as plt

plt.hist(student_scores, bins=10, edgecolor='black')
plt.title('Distribution of Student Scores')
plt.xlabel('Scores')
plt.ylabel('Frequency')
plt.show()
