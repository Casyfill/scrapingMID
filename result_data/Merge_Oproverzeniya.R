links <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/опровержения.csv"
texts <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/oproverzieniya_txt.csv"

df1 <- read.csv(links, header = T, sep = ",", stringsAsFactors = F)
df2 <- read.csv(texts, header = T, sep = ",", stringsAsFactors = F)

names(df1)
names(df2)
df3 <- merge(df1, df2, by='link')
names(df3)

outPath <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/oproverzheniye_merged.csv"
write.csv(df3, outPath)
