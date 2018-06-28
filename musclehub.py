
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[ ]:

# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query
import numpy as np


# In[ ]:

# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[ ]:

# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT *
FROM applications
LIMIT 5
''')
df.head()


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[ ]:

# Examine visits here
sql_query('''
select *
from visits
limit 5;''')


# In[5]:

# Examine fitness_tests here
sql_query('''
select *
from fitness_tests
limit 5;''')


# In[6]:

# Examine applications here
sql_query('''
select *
from applications
limit 5;''')


# In[7]:

# Examine purchases here
sql_query('''
select *
from purchases
limit 5;''')


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[8]:

df = sql_query('''
select  a.first_name as First_Name,
        a.last_name as Last_Name,
        a.gender as Gender,
        a.email as email,
        a.visit_date as Visit,
        b.fitness_test_date as Fitness_Test,
        c.application_date as Application,
        d.purchase_date as Purchase

from 

(select first_name, last_name, gender, email, visit_date
from visits
where visit_date >='7-1-17') a

left join 

(select first_name, last_name, email, fitness_test_date
from fitness_tests) b

on a.first_name = b.first_name
    and a.last_name = b.last_name
    and a.email = b.email
    
left join

(select first_name, last_name, email, application_date
from applications) c

on a.first_name = c.first_name
    and a.last_name = c.last_name
    and a.email = c.email
    
left join

(select first_name, last_name, email, purchase_date
from purchases) d

on a.first_name = d.first_name
    and a.last_name = d.last_name
    and a.email = d.email;
''')

print('Rows, Columns: {}'.format(df.shape))
print('Columns: {}'.format(', '.join(df.columns)))


# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[9]:

import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[10]:

df['AB_Test_Group'] = df['Fitness_Test'].apply(lambda x: 'B' if x == None else 'A')


# In[11]:

df.head()


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[12]:

ab_counts = df.groupby('AB_Test_Group').size().reset_index(name = 'Counts')
ab_counts


# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[13]:

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
            (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
            (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
            (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
            (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):    
   r, g, b = tableau20[i]    
   tableau20[i] = (r / 255., g / 255., b / 255.)

angle = 0
   
plt.figure(dpi=300, facecolor='w')
_, texts = plt.pie(ab_counts['Counts'],
       labels=['A: {:.1f}%'.format(
                   ab_counts.loc[0,'Counts'] * 100.0 / ab_counts['Counts'].sum() ),
               'B: {:.1f}%'.format(
                   ab_counts.loc[1,'Counts'] * 100.0 / ab_counts['Counts'].sum() )
              ],
       labeldistance = 0.88,
       colors = tableau20[::4],
       wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white' },
       startangle = angle
      )


for text in texts:
   text.set_color('white')
   text.set_fontweight('bold')
   text.set_rotation(angle)
   text.set_horizontalalignment('center')
   
plt.axis('equal')
p = plt.gcf()
p.gca().add_artist(plt.Circle( (0,0), 0.8, color='white'))
plt.title('Members of A/B Categories', y = 0.462, fontweight='bold', fontsize = 12)
plt.subplots_adjust(right=0.9)
plt.tight_layout()
plt.show()
plt.savefig('ab_test_pie_chart.png', dpi=600)
plt.close()


# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[14]:

df['is_application'] = df['Application'].apply(
    lambda x: 'Application' if x != None else 'No Application')


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[15]:

app_counts = df.groupby(['AB_Test_Group','is_application']).    First_Name.count().    reset_index(name = 'Count')
    
app_counts


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[16]:

app_pivot = app_counts.pivot(
    index = 'AB_Test_Group',
    columns = 'is_application',
    values = 'Count').\
    reset_index()
app_pivot


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[17]:

app_pivot['Total'] = app_pivot['Application'] + app_pivot['No Application']


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[18]:

app_pivot['Percent with Application'] = app_pivot['Application'] / app_pivot['Total']


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[19]:

app_pivot


# In[20]:

from scipy.stats import binom_test, chi2_contingency

p_val = binom_test(x = [app_pivot.loc[1,'Application'], app_pivot.loc[1,'No Application']],
           p = app_pivot.loc[0,'Percent with Application'], alternative='greater')


chi_p_val= chi2_contingency([app_pivot.loc[0,['Application','No Application']],
                 app_pivot.loc[1,['Application','No Application']]])[1]


print('p-value: {:.6f} | {:.6f} - '.format(p_val, chi_p_val)),
if p_val > 0.05 or chi_p_val > 0.05:
    print('null hypothesis cannot be rejected.')
else:
    print('null hypothesis can be rejected!\nSignficant difference from untreated group (A).')


# ## Step 4: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[21]:

df['is_member'] = df['Purchase'].apply(
                    lambda x: 'Member' if x != None else 'Not Member')


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[22]:

just_apps = df[df['is_application'] == 'Application']
just_apps.head()


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[23]:

member_pivot = just_apps.groupby(['is_member','AB_Test_Group']).    First_Name.count().    reset_index(name = 'Count').pivot(
    index = 'AB_Test_Group',
    columns = 'is_member',
    values = 'Count').\
    reset_index()
    
member_pivot['Total'] = member_pivot['Member'] + member_pivot['Not Member']
member_pivot['Percent Purchase'] = member_pivot['Member'] / member_pivot['Total']
member_pivot


# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[24]:

p_val = binom_test(
        x = [member_pivot.loc[1,'Member'], member_pivot.loc[1,'Not Member']],
        p = member_pivot.loc[0,'Percent Purchase'], alternative='greater')


chi_p_val= chi2_contingency([member_pivot.loc[0,['Member','Not Member']],
                 member_pivot.loc[1,['Member','Not Member']]])[1]


print('p-value: {:.6f} | {:.6f} - '.format(p_val, chi_p_val)),
if p_val > 0.05 or chi_p_val > 0.05:
    print('null hypothesis cannot be rejected.')
else:
    print('null hypothesis can be rejected!\nSignficant difference from untreated group. (A)')


# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[25]:

final_member_pivot = df.groupby(['is_member','AB_Test_Group']).    First_Name.count().    reset_index(name = 'Count').pivot(
    index = 'AB_Test_Group',
    columns = 'is_member',
    values = 'Count').\
    reset_index()
    
final_member_pivot['Total'] = final_member_pivot['Member'] +                                final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = final_member_pivot['Member'] /                                final_member_pivot['Total']
final_member_pivot


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# In[26]:

p_val = binom_test(
        x = [final_member_pivot.loc[1,'Member'], final_member_pivot.loc[1,'Not Member']],
        p = final_member_pivot.loc[0,'Percent Purchase'], alternative='greater')


chi_p_val= chi2_contingency([final_member_pivot.loc[0,['Member','Not Member']],
                 final_member_pivot.loc[1,['Member','Not Member']]])[1]


print('p-value: {:.6f} | {:.6f} - '.format(p_val, chi_p_val)),
if p_val > 0.05 or chi_p_val > 0.05:
    print('null hypothesis cannot be rejected.')
else:
    print('null hypothesis can be rejected!\nSignficant difference from untreated group. (A)')


# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[27]:

ax = plt.subplot()
plt.bar(
    range(app_pivot.shape[0]),
    app_pivot['Percent with Application']*100,
    yerr = None,
    capsize=5,
    color = tableau20[5],
    alpha = 1)
plt.title('Percentage of Visitors Who Apply', fontsize=16, y = 1.1)
ax.set_xticks(range(app_pivot.shape[0]))
ax.set_yticks(range(0,int(app_pivot['Percent with Application'].max()*100 + 10),5))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_ylabel('Applied (%)', fontsize=14)
ax.set_xlabel('Test Group', fontsize=14)
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)
plt.xticks(fontsize=14, rotation=0)  
plt.yticks(fontsize=14) 
plt.show


# In[28]:

ax = plt.subplot()
plt.bar(
    range(member_pivot.shape[0]),
    member_pivot['Percent Purchase']*100,
    yerr = None,
    capsize=5,
    color = tableau20[7],
    alpha = 1)
plt.title('Percentage of Applicants Who Become Members', fontsize=16, y = 1.1)
ax.set_xticks(range(member_pivot.shape[0]))
ax.set_yticks(range(0,int(member_pivot['Percent Purchase'].max()*100 + 10),10))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_ylabel('Members (%)', fontsize=14)
ax.set_xlabel('Test Group', fontsize=14)
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)
plt.xticks(fontsize=14, rotation=0)  
plt.yticks(fontsize=14) 
plt.show


# In[29]:

ax = plt.subplot()
plt.bar(
    range(final_member_pivot.shape[0]),
    final_member_pivot['Percent Purchase']*100,
    yerr = None,
    capsize=5,
    color = tableau20[9],
    alpha = 1)
plt.title('Percentage of Visitors Who Become Members', fontsize=16, y = 1.1)
ax.set_xticks(range(final_member_pivot.shape[0]))
ax.set_yticks(range(0,int(final_member_pivot['Percent Purchase'].max()*100 + 10),5))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_ylabel('Members (%)', fontsize=14)
ax.set_xlabel('Test Group', fontsize=14)
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)
plt.xticks(fontsize=14, rotation=0)  
plt.yticks(fontsize=14) 
plt.show


# ## Show Funnel

# In[30]:

a = [
    app_pivot[app_pivot['AB_Test_Group'] == 'A']['Total'].values[0],
    app_pivot[app_pivot['AB_Test_Group'] == 'A']['Application'].values[0],
    final_member_pivot[final_member_pivot['AB_Test_Group'] == 'A']['Member'].values[0],
]

b = [
    app_pivot[app_pivot['AB_Test_Group'] == 'B']['Total'].values[0],
    app_pivot[app_pivot['AB_Test_Group'] == 'B']['Application'].values[0],
    final_member_pivot[final_member_pivot['AB_Test_Group'] == 'B']['Member'].values[0],
]
a,b


# In[31]:

ax = plt.subplot()
plt.plot(
    range(len(a)),
    a,
    color = tableau20[0],
    alpha = 1,
    marker = 'o',
    label = 'Fitness Test')
plt.plot(
    range(len(b)),
    b,
    color = tableau20[4],
    alpha = 1,
    linestyle= '--',
    marker = 'o',
    label = 'No Fitness Test')
plt.title('Visitors in Each Test Group', fontsize=16, y = 1.1)
ax.set_xticks(range(len(a)))
ax.set_yticks(range(0,int(max(max(a,b))*1.10),int(round(max(max(a,b))*.1,-2))))
ax.set_xticklabels(['Vistors in Group','Applications', 'Members'])
ax.set_ylabel('Number', fontsize=14)
ax.set_xlabel('Step in Funnel', fontsize=14, fontweight = 'bold')
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)
plt.xticks(fontsize=14, rotation=0)  
plt.yticks(fontsize=14) 
plt.legend()
plt.show


# In[36]:

a_flow = [app_pivot[app_pivot['AB_Test_Group'] == 'A']['Total'].values[0],
         -app_pivot[app_pivot['AB_Test_Group'] == 'A']['No Application'].values[0],
         -member_pivot[member_pivot['AB_Test_Group'] == 'A']['Not Member'].values[0],
         -final_member_pivot[final_member_pivot['AB_Test_Group'] == 'A']\
          ['Member'].values[0]]
#a_flow = [float(x) * 100 / a_flow[0] for x  in a_flow]

b_flow = [app_pivot[app_pivot['AB_Test_Group'] == 'B']['Total'].values[0],
         -member_pivot[member_pivot['AB_Test_Group'] == 'B']['Not Member'].values[0],
         -app_pivot[app_pivot['AB_Test_Group'] == 'B']['No Application'].values[0],
         -final_member_pivot[final_member_pivot['AB_Test_Group'] == 'B']\
          ['Member'].values[0]]
#b_flow = [float(x) * 100/ b_flow[0] for x  in b_flow]

a_flow, b_flow


# In[34]:

from matplotlib.sankey import Sankey


# In[42]:

labels = ['', 'Did Not Apply', 'Applied but\nDid Not\nBecome Member' , 'Became\nMember']
labels2 = ['', 'Applied but\nDid Not\nBecome Member', 'Did Not Apply', 'Became\nMember']

plt.close()


fig = plt.figure(figsize=(7,7.2), dpi=600, frameon=False)

ax = fig.add_subplot(2, 1, 1, xticks=[], yticks=[], frameon=False,)
ax.set_title("Flow Diagram of MuscleHub Visitors",y = 1.1, fontweight='bold')
ax2 = fig.add_subplot(2,1,2, xticks=[], yticks=[], frameon=False,)

sankey = Sankey(ax=ax, scale=0.0005, offset=0.65, head_angle=120,
                format = '%d', unit=' visitors', gap=1, 
                radius=0.05, shoulder=0.05,)
sankey.add(flows = a_flow,
            labels = labels,
            orientations= [0, 1, 1, 0],
            pathlengths=[0, 1, 2.5, 1],
            trunklength=5.,
            facecolor=tableau20[0],
            label="Fitness Test"
          ).finish()

sankey2 = Sankey(ax=ax2, scale=0.0005, offset=0.65, head_angle=120,
                format = '%d', unit=' visitors', gap=1, 
                radius=0.04, shoulder=0.05,)
sankey2.add(flows = b_flow,
            labels = labels2,
            orientations= [0, -1, -1, 0],
            pathlengths=[0, 2.5, 1, 1],
            trunklength=5.,
            facecolor=tableau20[4],
            label="No Fitness Test"
          ).finish()

ax.text(0.25, 0.25, 'Fitness Test', horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes, fontweight='bold')
ax2.text(0.25, -0.3, 'No Fitness Test', horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes, fontweight='bold')

plt.tight_layout()
plt.show()

