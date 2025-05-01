'''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("data.csv")
clean_data = data.dropna(subset=['% change in abortion rate, 2017-2020', '% of counties without a known clinic, 2020'])

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='% of counties without a known clinic, 2020',
    y='% change in abortion rate, 2017-2020',
    data=clean_data,
    hue=clean_data['% of counties without a known clinic, 2020'] > 90,
    palette={True: 'red', False: 'blue'},
    s=100
)
sns.regplot(
    x='% of counties without a known clinic, 2020',
    y='% change in abortion rate, 2017-2020',
    data=clean_data,
    scatter=False,
    color='black',
    line_kws={'linestyle': '--'}
)
plt.title("Stricter Clinic Regulations Correlate with Fewer Abortions", pad=20)
plt.xlabel("% of Counties Without a Clinic (2020)")
plt.ylabel("% Change in Abortion Rate (2017-2020)")
plt.legend(title='>90% Clinic Scarcity', labels=['No', 'Yes'])
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig("vis1_pro.png", dpi=300)

highlight_states = ['Missouri', 'Mississippi', 'Wyoming']
highlight_data = clean_data[clean_data['U.S. State'].isin(highlight_states)]

plt.figure(figsize=(10, 6))
bars = plt.bar(
    highlight_data['U.S. State'],
    highlight_data['% change in abortion rate, 2017-2020'],
    color=['firebrick' if x < 0 else 'steelblue' for x in highlight_data['% change in abortion rate, 2017-2020']]
)
plt.axhline(0, color='black', linestyle='--')
plt.title("Extreme Declines in States with Clinic Restrictions", pad=20)
plt.ylabel("% Change in Abortion Rate (2017-2020)")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height/2, f"{height:.0f}%", 
             ha='center', va='center', color='white', weight='bold')
plt.tight_layout()
plt.savefig("vis2_pro.png", dpi=300)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='% of counties without a known clinic, 2020',
    y='No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020',
    data=clean_data,
    size='No. of abortions, by state of occurrence, 2020',
    sizes=(50, 500),
    alpha=0.7,
    color='green'
)
plt.title("Abortion Rates Persist Even Where Clinics Are Scarce", pad=20)
plt.xlabel("% of Counties Without a Clinic (2020)")
plt.ylabel("Abortion Rate per 1,000 Women (2020)")
plt.legend(title='Total Abortions (2020)', bbox_to_anchor=(1.05, 1))
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig("vis1_anti.png", dpi=300)


outliers = clean_data.nlargest(3, '% of counties without a known clinic, 2020')
plt.figure(figsize=(10, 6))
sns.barplot(
    x='U.S. State',
    y='No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020',
    data=outliers,
    palette='viridis'
)
plt.title("High Clinic Scarcity Doesn't Always Reduce Abortions", pad=20)
plt.ylabel("Abortion Rate per 1,000 Women (2020)")
for i, rate in enumerate(outliers['No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020']):
    plt.text(i, rate/2, f"{rate:.1f}", ha='center', va='center', color='white', weight='bold')
plt.tight_layout()
plt.savefig("vis2_anti.png", dpi=300)


plt.figure(figsize=(10,6))
sns.scatterplot(
    x='Change in the no. of abortion clinics, 2017-2020',
    y='% change in abortion rate, 2017-2020',
    data=data,
    hue=data['Change in the no. of abortion clinics, 2017-2020'] < 0,
    palette={True:'red', False:'green'},
    s=100
)
plt.axvline(0, color='black', linestyle=':')
plt.axhline(0, color='black', linestyle=':')
plt.title("States Losing Clinics Saw Greater Abortion Declines", pad=20)
plt.xlabel("Change in Number of Clinics (2017-2020)")
plt.ylabel("% Change in Abortion Rate (2017-2020)")
plt.legend(title='Lost Clinics?', labels=['Gained Clinics', 'Lost Clinics'])
plt.annotate('Missouri', xy=(-2, -98), xytext=(-15, -80),
             arrowprops=dict(arrowstyle='->'))
plt.grid(alpha=0.3)
plt.tight_layout()


travel_data = data.dropna(subset=['% of residents obtaining abortions who traveled out of state for care, 2020'])
plt.figure(figsize=(10,6))
sns.regplot(
    x='% of counties without a known clinic, 2020',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=travel_data,
    scatter_kws={'s':100, 'alpha':0.7},
    line_kws={'color':'red'}
)
plt.title("More Clinic Scarcity Forces More Women to Travel Out-of-State", pad=20)
plt.xlabel("% of Counties Without a Clinic (2020)")
plt.ylabel("% of Abortion Patients Traveling Out-of-State")
plt.grid(alpha=0.3)
plt.tight_layout()


funding_data = data[['U.S. State', 'Reported public expenditures for abortions (in 000s of dollars), state, 2015',
                    '% of counties without a known clinic, 2020']].dropna()
funding_data = funding_data.nlargest(10, 'Reported public expenditures for abortions (in 000s of dollars), state, 2015')

plt.figure(figsize=(10,6))
sns.barplot(
    x='Reported public expenditures for abortions (in 000s of dollars), state, 2015',
    y='U.S. State',
    data=funding_data,
    palette='Blues_r'
)
plt.title("States With Highest Public Abortion Funding Still Have Clinic Deserts", pad=20)
plt.xlabel("State Funding (Thousands of $, 2015)")
plt.ylabel("")
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()


rate_data = data[['U.S. State', 'No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020',
                 '% of counties without a known clinic, 2020']].dropna()
rate_data['Clinic Access'] = pd.cut(rate_data['% of counties without a known clinic, 2020'],
                                   bins=[0,50,90,100],
                                   labels=['Good','Moderate','Poor'])

plt.figure(figsize=(10,6))
sns.boxplot(
    x='Clinic Access',
    y='No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020',
    data=rate_data,
    palette='Oranges'
)
plt.title("Abortion Rates Show Minimal Variation Across Clinic Access Levels", pad=20)
plt.xlabel("Clinic Access by County Coverage")
plt.ylabel("Abortion Rate per 1,000 Women (2020)")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv("data.csv")
'''
# Advanced data transformation
data['Clinic Access Tier'] = pd.cut(data['% of counties without a known clinic, 2020'],
                                   bins=[0, 50, 90, 100],
                                   labels=['Good (0-50%)', 'Moderate (50-90%)', 'Severe (90-100%)'])
data['Size'] = np.log(data['No. of abortions, by state of occurrence, 2020']) * 10

# Create figure with multiple coordinated views
plt.figure(figsize=(14, 6))
grid = plt.GridSpec(1, 3, width_ratios=[3, 1, 1])

# Main scatter plot
plt.subplot(grid[0])
scatter = sns.scatterplot(
    x='% of counties without a known clinic, 2020',
    y='% change in abortion rate, 2017-2020',
    hue='Clinic Access Tier',
    size='Size',
    sizes=(50, 300),
    palette=['#4daf4a', '#377eb8', '#e41a1c'],
    alpha=0.8,
    data=data.dropna(subset=['% change in abortion rate, 2017-2020']))
plt.title("Clinic Scarcity Strongly Predicts Abortion Rate Declines\n(2017-2020)", pad=20, fontsize=14)
plt.xlabel("% of Counties Without Abortion Clinics (2020)", fontsize=12)
plt.ylabel("% Change in Abortion Rate (2017-2020)", fontsize=12)
plt.axhline(0, color='black', linestyle=':')
handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles[:4], labels[:4], title='Clinic Access Tier', bbox_to_anchor=(1.05, 1))

# Annotations
plt.annotate('Missouri\n(-98%)', xy=(99, -98), xytext=(85, -80),
             arrowprops=dict(arrowstyle="->", color='black'),
             bbox=dict(boxstyle="round", fc="white", ec="black"))
plt.annotate('More clinics →\nSmaller declines', xy=(10, 20), 
             ha='center', fontsize=10)

# Supplemental boxplot
plt.subplot(grid[1])
sns.boxplot(
    y='% change in abortion rate, 2017-2020',
    x='Clinic Access Tier',
    data=data,
    palette=['#4daf4a', '#377eb8', '#e41a1c'],
    order=['Good (0-50%)', 'Moderate (50-90%)', 'Severe (90-100%)']
)
plt.title("Distribution by Access Tier", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.xlabel("")

# Supplemental bar chart
plt.subplot(grid[2])
travel_data = data.nlargest(5, '% of residents obtaining abortions who traveled out of state for care, 2020')
sns.barplot(
    y='U.S. State',
    x='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=travel_data,
    palette='Reds_r'
)
plt.title("Top 5 States for\nOut-of-State Travel", fontsize=12)
plt.xlabel("% Traveling Out-of-State")

plt.tight_layout()
plt.show()
plt.savefig("enhanced_pro_visual1.png", dpi=300, bbox_inches='tight')
'''
'''# Create restriction index
data['Restriction_Index'] = (
    (data['% of counties without a known clinic, 2020'] > 90).astype(int) +
    (data['No. of abortion clinics, 2020'] < 5).astype(int)
)

plt.figure(figsize=(10,6))
sns.boxplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    palette='Reds'
)
plt.title("More Restrictions = More Out-of-State Travel", pad=20)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

plt.figure(figsize=(12, 7))
sns.regplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    scatter_kws={'s': 100, 'alpha': 0.7, 'color': 'steelblue'},
    line_kws={'color': 'red', 'linestyle': '--', 'label': 'Trend'},
    ci=None
)
plt.title("Abortion Restrictions Show No Clear Link to Out-of-State Travel", pad=20, fontsize=14)
plt.xlabel("Restriction Index (Higher = More Restrictions)", fontsize=12)
plt.ylabel("% Patients Traveling Out-of-State", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Highlight outliers (e.g., states with high travel despite low restrictions)
outliers = data[data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 30]
for i, row in outliers.iterrows():
    plt.text(row['Restriction_Index'] + 0.05, row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
             row['U.S. State'], ha='left', va='center', fontsize=9)

plt.show()

plt.figure(figsize=(12, 7))

# Filter data to only include restriction indexes 0, 1, 2
filtered_data = data[data['Restriction_Index'].isin([0, 1, 2])]

sns.regplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=filtered_data,
    scatter_kws={'s': 100, 'alpha': 0.7, 'color': 'steelblue'},
    line_kws={'color': 'red', 'linestyle': '--', 'label': 'Trend'},
    ci=None,
    x_jitter=0.1  # Adds slight jitter to separate overlapping points
)

# Set explicit x-axis limits and ticks
plt.xlim(-0.5, 2.5)
plt.xticks([0, 1, 2], ['0 (Least Restricted)', '1', '2 (Most Restricted)'])

plt.title("Abortion Restrictions Show No Clear Link to Out-of-State Travel", pad=20, fontsize=14)
plt.xlabel("Restriction Index (Higher = More Restrictions)", fontsize=12)
plt.ylabel("% Patients Traveling Out-of-State", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Highlight outliers (e.g., states with high travel despite low restrictions)
outliers = filtered_data[filtered_data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 30]
for i, row in outliers.iterrows():
    plt.text(row['Restriction_Index'] + 0.05, 
             row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
             row['U.S. State'], 
             ha='left', 
             va='center', 
             fontsize=9,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

plt.show()

plt.figure(figsize=(12, 7))

# Filter data and remove most outliers for index 1 and 2
filtered_data = data[
    data['Restriction_Index'].isin([0, 1, 2]) & 
    ~(
        (data['Restriction_Index'].isin([1, 2]) & 
        (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 15)
    ))
]

# Keep specific important outliers that challenge the narrative
important_outliers = data[
    (data['U.S. State'].isin(['Alabama', 'Mississippi', 'South Carolina'])) |
    (data['Restriction_Index'] == 0) & 
    (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20)
]

# Combine filtered data with important outliers
plot_data = pd.concat([filtered_data, important_outliers]).drop_duplicates()

sns.regplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=plot_data,
    scatter_kws={'s': 100, 'alpha': 0.7, 'color': 'steelblue'},
    line_kws={'color': 'red', 'linestyle': '--', 'label': 'Trend'},
    ci=None,
    x_jitter=0.1
)

# Set explicit x-axis limits and ticks
plt.xlim(-0.5, 2.5)
plt.xticks([0, 1, 2], ['0 (Least Restricted)', '1', '2 (Most Restricted)'])

plt.title("Most States Show Minimal Travel Despite Restrictions", pad=20, fontsize=14)
plt.xlabel("Restriction Index (Higher = More Restrictions)", fontsize=12)
plt.ylabel("% Patients Traveling Out-of-State", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Highlight only the most important outliers
key_outliers = plot_data[plot_data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20]
for i, row in key_outliers.iterrows():
    plt.text(row['Restriction_Index'] + 0.05, 
             row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
             row['U.S. State'], 
             ha='left', 
             va='center', 
             fontsize=9,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# Add annotation explaining the pattern
plt.annotate('Majority of states with stricter abortion rules show similar travel rates\nas less restricted states',
             xy=(1, 10), xytext=(0.5, 30),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="w"))

plt.show()

# Enhanced data transformation - weighted restriction index
data['Weighted_Restriction'] = ((data['% of counties without a known clinic, 2020']/100) + 
    (1 - (data['No. of abortion clinics, 2020']/data['No. of abortion clinics, 2020'].max())))
data['Restriction_Tier'] = pd.qcut(data['Weighted_Restriction'], q=3, labels=['Low', 'Medium', 'High'])

plt.figure(figsize=(12,7))
ax = sns.boxplot(
    x='Restriction_Tier',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    palette=['#ffcccc', '#ff6666', '#cc0000'],  # Progressive red intensity
    width=0.6,
    linewidth=1.5,
    fliersize=0  # Hide outliers for cleaner look
)

# Add actual data points with jitter
sns.stripplot(
    x='Restriction_Tier',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    color='black',
    alpha=0.4,
    size=6,
    jitter=0.2
)

# Emphasize trend with annotation
plt.annotate('Clear Trend: Higher Restrictions → More Out-of-State Travel', 
             xy=(2, 35), xytext=(1, 45),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="white"),
             fontsize=12)

# Improved labels and title
plt.title("Abortion Restrictions Strongly Correlate With Increased Out-of-State Travel", 
          pad=20, fontsize=16, fontweight='bold')
plt.xlabel("Restriction Level (Weighted Index)", fontsize=12)
plt.ylabel("Percentage Traveling Out-of-State", fontsize=12)
plt.ylim(0, 60)

# Add median labels
medians = data.groupby('Restriction_Tier')['% of residents obtaining abortions who traveled out of state for care, 2020'].median()
for xtick in ax.get_xticks():
    ax.text(xtick, medians[xtick]+2, f"Median: {medians[xtick]:.1f}%", 
            horizontalalignment='center', 
            fontsize=11,
            bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

# Create access score combining multiple factors
data['Access_Score'] = (
    (data['No. of abortion clinics, 2020']/data['No. of abortion clinics, 2020'].max()) + 
    (1 - data['% of women aged 15-44 living in a county without a clinic, 2020']/100)
)

plt.figure(figsize=(12,7))
ax = sns.scatterplot(
    x='Access_Score',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    hue='Restriction_Index',
    size='No. of abortion clinics, 2020',
    data=data,
    palette='Blues_r',
    sizes=(50, 300),
    alpha=0.8
)

# Add trend line for access score only
sns.regplot(
    x='Access_Score',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    scatter=False,
    color='red',
    line_kws={'linestyle':'--', 'alpha':0.5},
    ci=None
)

# Strategic annotations
plt.annotate('Access Barriers Better Predict Travel\nThan Restriction Laws Alone', 
             xy=(0.4, 40), xytext=(0.2, 50),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="white"),
             fontsize=12)

# Highlight key counter-examples
counter_examples = data[data['U.S. State'].isin(['Texas', 'Georgia', 'Delaware'])]
for i, row in counter_examples.iterrows():
    plt.text(row['Access_Score']+0.02, row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
             row['U.S. State'], 
             fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8))

# Improved labels and title
plt.title("Clinic Access—Not Restrictions—Drives Out-of-State Abortion Travel", 
          pad=20, fontsize=16, fontweight='bold')
plt.xlabel("Healthcare Access Score (Clinic Availability + Geographic Coverage)", fontsize=12)
plt.ylabel("Percentage Traveling Out-of-State", fontsize=12)
plt.legend(title='Restriction Index', bbox_to_anchor=(1.05, 1))
plt.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()
# Keep original restriction index calculation
data['Restriction_Index'] = (
    (data['% of counties without a known clinic, 2020'] > 90).astype(int) +
    (data['No. of abortion clinics, 2020'] < 5).astype(int)
)

plt.figure(figsize=(10.5,6.5))  # Slightly larger

# Enhanced boxplot with subtle improvements
ax = sns.boxplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    palette=['#ffcccc','#ff6666','#cc0000'],  # Gradient reds
    width=0.55,
    linewidth=1.5,
    fliersize=5  # Smaller outlier dots
)

# Add subtle data points with jitter
sns.stripplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    color='black',
    alpha=0.4,
    size=4,
    jitter=0.2
)

# Add median value labels
medians = data.groupby('Restriction_Index')['% of residents obtaining abortions who traveled out of state for care, 2020'].median()
for idx in medians.index:
    ax.text(idx, medians[idx]-2, f"Median: {medians[idx]:.1f}%", 
            ha='center', va='top', fontsize=9,
            bbox=dict(facecolor='white', alpha=0.8, pad=2))

# Improved title and labels
plt.title("Abortion Restrictions Consistently Increase Out-of-State Travel", 
          pad=18, fontsize=13, fontweight='semibold')
plt.xlabel("\nRestriction Index (Higher = More Restrictions)", fontsize=11)
plt.ylabel("Percentage Traveling Out-of-State\n", fontsize=11)
plt.ylim(0, 60)

# Add subtle grid
plt.grid(axis='y', alpha=0.2, linestyle=':')

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 7))

# Keep original filtering approach
filtered_data = data[
    data['Restriction_Index'].isin([0, 1, 2]) & 
    ~((data['Restriction_Index'].isin([1, 2]) & 
       (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 15))
    )
]
important_outliers = data[
    (data['U.S. State'].isin(['Alabama', 'Mississippi', 'South Carolina'])) |
    ((data['Restriction_Index'] == 0) & 
     (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20))
]
plot_data = pd.concat([filtered_data, important_outliers]).drop_duplicates()

# Enhanced scatterplot
ax = sns.regplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=plot_data,
    scatter_kws={'s': 90, 'alpha': 0.7, 'color': 'steelblue', 'edgecolor':'white', 'linewidth':0.5},
    line_kws={'color': 'red', 'linestyle': '--', 'label': 'Trend', 'alpha':0.7},
    ci=None,
    x_jitter=0.12
)

# Set axis limits and ticks
plt.xlim(-0.5, 2.5)
plt.xticks([0, 1, 2], ['0 (Least Restricted)', '1', '2 (Most Restricted)'])
plt.ylim(-2, 60)

# Highlight outliers with more emphasis
key_outliers = plot_data[plot_data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20]
for i, row in key_outliers.iterrows():
    ax.scatter(row['Restriction_Index'], 
               row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
               color='red', s=100, edgecolor='black', linewidth=1, zorder=10)
    plt.text(row['Restriction_Index'] + 0.07, 
             row['% of residents obtaining abortions who traveled out of state for care, 2020']+1, 
             row['U.S. State'], 
             ha='left', 
             va='bottom', 
             fontsize=9,
             bbox=dict(facecolor='white', alpha=0.8, pad=2))

# Improved annotation
plt.annotate('Most states show similar travel rates\nregardless of restriction level',
             xy=(1, 10), xytext=(0.5, 30),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="steelblue"),
             fontsize=10)

# Professional title and labels
plt.title("Abortion Restrictions Show Minimal Impact on Out-of-State Travel Patterns", 
          pad=18, fontsize=13, fontweight='semibold')
plt.xlabel("Restriction Index (Higher = More Restrictions)", fontsize=11)
plt.ylabel("Percentage Traveling Out-of-State", fontsize=11)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.15, linestyle=':')

plt.tight_layout()
plt.show()'''

data['Restriction_Index'] = (
    (data['% of counties without a known clinic, 2020'] > 90).astype(int) +
    (data['No. of abortion clinics, 2020'] < 5).astype(int)
)

plt.figure(figsize=(12,7))
sns.boxplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    palette='Reds',
    width=0.4,
    fliersize=4
)
plt.title("More Restrictions = More Out-of-State Travel for Abortions", pad=20)
plt.xlabel("Restriction Index (Higher = More Restrictions on Abortions)")
plt.ylabel("% of Patients Traveling Out-of-State")

plt.savefig("vis_pro.png", dpi=300)
plt.show()

data['Restriction_Index'] = (
    (data['% of counties without a known clinic, 2020'] > 90).astype(int) +
    (data['No. of abortion clinics, 2020'] < 5).astype(int)
)

plt.figure(figsize=(12,7))
ax = sns.boxplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=data,
    palette='Reds',
    width=0.4,
    fliersize=4,
    linewidth=1.5  # Thicker lines for better visibility
)

plt.title("More Restrictions = More Out-of-State Travel for Abortions", pad=20, fontsize=14, fontweight='bold')
plt.xlabel("Restriction Index (Higher = More Restrictions on Abortions)", fontsize=12)
plt.ylabel("% of Patients Traveling Out-of-State", fontsize=12)

# Calculate and annotate median values
medians = data.groupby('Restriction_Index')['% of residents obtaining abortions who traveled out of state for care, 2020'].median()
for idx, med in enumerate(medians):
    ax.text(idx, med+1, f"Median: {med:.1f}%", 
            ha='center', va='bottom', fontsize=11,
            bbox=dict(facecolor='white', alpha=0.8, pad=2))

# Highlight trend with arrow annotation
plt.annotate('Clear Increasing Trend',
             xy=(2, medians[2]), xytext=(1, medians[2]+15),
             arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
             bbox=dict(boxstyle="round", fc="white", ec="red", pad=0.5),
             fontsize=12)


# Add explanatory note
plt.text(0.5, 85, "Note: Each increasing restriction level shows higher median out-of-state travel rates",
         ha='center', va='center', fontsize=10, color='red')

plt.grid(axis='y', alpha=0.2)  # Light grid for better readability
plt.tight_layout()
plt.savefig("vis_pro.png", dpi=300, bbox_inches='tight')
plt.show()


plt.figure(figsize=(12, 7))
# Filter data and remove most outliers for index 1 and 2
filtered_data = data[
    data['Restriction_Index'].isin([0, 1, 2]) & 
    ~(
        (data['Restriction_Index'].isin([1, 2]) & 
        (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 15)
    ))
]

# Keep specific important outliers that challenge the narrative
important_outliers = data[
    (data['U.S. State'].isin(['Alabama', 'Mississippi', 'South Carolina'])) |
    (data['Restriction_Index'] == 0) & 
    (data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20)
]

# Combine filtered data with important outliers
plot_data = pd.concat([filtered_data, important_outliers]).drop_duplicates()

sns.regplot(
    x='Restriction_Index',
    y='% of residents obtaining abortions who traveled out of state for care, 2020',
    data=plot_data,
    scatter_kws={'s': 100, 'alpha': 0.7, 'color': 'steelblue'},
    line_kws={'color': 'red', 'linestyle': '--', 'label': 'Trend'},
    ci=None,
    x_jitter=0.1,
    robust=True
)

# Set explicit x-axis limits and ticks
plt.xlim(-0.5, 2.5)
plt.xticks([0, 1, 2], ['0 (Least Restricted)', '1', '2 (Most Restricted)'])

plt.title("Most States Show Minimal Travel Despite Restrictions", pad=20, fontsize=14)
plt.xlabel("Restriction Index (Higher = More Abortion Restrictions)", fontsize=12)
plt.ylabel("% Patients Traveling Out-of-State", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Highlight only the most important outliers
key_outliers = plot_data[plot_data['% of residents obtaining abortions who traveled out of state for care, 2020'] > 20]
for i, row in key_outliers.iterrows():
    x_offset = 0.15
    y_offset = 1
    
    # Special adjustment for South Carolina
    if row['U.S. State'] == 'South Carolina':
        x_offset = 0.2
        y_offset = 1.5
    if row['U.S. State'] == 'District of Columbia':
        x_offset = 0.2
        y_offset = 1.5
  
    plt.text(row['Restriction_Index'] + 0.05, 
             row['% of residents obtaining abortions who traveled out of state for care, 2020'], 
             row['U.S. State'], 
             ha='left', 
             va='center', 
             fontsize=9,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# Add annotation explaining the pattern
plt.annotate('Majority of states with stricter abortion rules show similar travel rates\nas less restricted states',
             xy=(1, 10), xytext=(0.5, 30),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="w"))
plt.savefig("vis_anti.png", dpi=300)
plt.show()

