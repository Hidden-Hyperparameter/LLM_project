import random
tags = [
    'math', 'english', 'science', 'history', 'geography', 'physics', 'chemistry', 'biology', 'astronomy', 'computer science',
    'programming', 'python', 'java', 'c++', 'javascript', 'html', 'css', 'data science', 'machine learning', 'artificial intelligence',
    'statistics', 'calculus', 'algebra', 'geometry', 'trigonometry', 'probability', 'discrete math', 'linear algebra', 'number theory',
    'real analysis', 'complex analysis', 'differential equations', 'numerical analysis', 'operations research', 'combinatorics', 'graph theory',
    'topology', 'set theory', 'logic', 'probability theory', 'stochastic processes', 'mathematical physics', 'optimization', 'cryptography',
    'game theory', 'computation', 'algorithms', 'theoretical computer science', 'computational geometry', 'quantum computing', 'data analysis',
    'statistical learning', 'regression analysis', 'multivariate analysis', 'time series analysis', 'bayesian statistics', 'statistical inference',
    'nonparametric statistics', 'biostatistics', 'actuarial science', 'financial mathematics', 'econometrics', 'dynamical systems', 'chaos theory',
    'fractal geometry', 'fourier analysis', 'wavelets', 'harmonic analysis', 'integral transforms', 'functional analysis', 'partial differential equations',
    'fluid dynamics', 'solid mechanics', 'celestial mechanics', 'numerical methods', 'monte carlo methods', 'simulation', 'modeling', 'control theory',
    'systems theory', 'information theory', 'coding theory', 'cryptanalysis', 'network theory', 'queueing theory', 'inventory theory', 'decision analysis',
    'social choice theory', 'voting theory', 'mechanism design', 'optimization algorithms', 'heuristics', 'metaheuristics', 'integer programming',
    'linear programming', 'nonlinear programming', 'convex optimization', 'global optimization', 'dynamic programming', 'stochastic programming',
    'approximation algorithms', 'randomized algorithms', 'combinatorial optimization', 'network optimization', 'continuous optimization',
    'variational calculus', 'optimal control', 'stochastic control', 'adaptive control', 'robust control', 'nonlinear control', 'h-infinity control',
    'fractional calculus', 'fuzzy mathematics'
]
tags2=[]
for tag in tags:
    tags2.append(tag.replace(' ', '_'))

final_tags = tags + tags2
f = open('/ssdshare/2024040125_2023040165_2023040163_project/src/file_search_wzh/test.txt', 'w')
for i in range(50):
    # generate a random string R
    R = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789_', k=random.randint(5, 15)))
    file_name = R + ".pdf"
    tags = random.sample(final_tags, random.randint(3, 10))
    string = 'File:'+ file_name + ',\ttags: '+ '; '.join(tags)
    f.write(string + '\n')


