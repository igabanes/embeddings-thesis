library(readr)
library(ggplot2)

results <- read.csv("results_wordsim353_0.csv")
data <- data.frame(results)

corr <- round(cor(data[3], data[4:21], method = "spearman"),2)
print(corr)

correlation <- as.vector(corr)
window <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50)
df <- data.frame(correlation, window)  
print(df)
ggplot(df, aes(x = window, y = correlation)) +
         geom_line() +
         geom_point() +
         ylim(0, 1) +
         xlab("window size") +
         geom_vline(xintercept = 35) +
         ggtitle("WordSim-353 (asymmetrical window)")
