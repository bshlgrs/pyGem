import matplotlib.pyplot as plt

data = [[0,0,0,6,5],[0,0,2,3,6],[0,0,0,1,10],[0,0,0,3,8],[0,1,0,1,9],[0,0,0,1,8]]
titles = ["GEM's interface was easy to learn",
          "I preferred using GEM to working by hand",
          "Uncertainties are easier in GEM than when working by hand",
          "GEM let me work faster than doing the problems by hand",
          "GEM let me work more accurately than\ndoing the problems by hand",
          "GEM lets me work faster than Mathematica would have"
          ]

for (datum, title) in zip(data,titles):
    plt.bar([1,2,3,4,5],datum, width=0.5, align='center')

    plt.xlim(xmin=0.5)
    plt.xlim(xmax=5.5)

    plt.ylabel("Number of respondents",size="large")

    plt.title(title,size = 'x-large')

    plt.savefig(title.replace(" ","_")+".png",transparent=True)
    plt.clf()