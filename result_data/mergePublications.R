links <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/publications_links.csv"
texts <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/publications_txt2.csv"

df1 <- read.csv(links, header = T, sep = ",", stringsAsFactors = F)
df2 <- read.csv(texts, header = T, sep = ",", stringsAsFactors = F)

names(df2)
df3 <- merge(df1, df2, by='link')
names(df3)

df4<- subset(df3, select=-c(text.x))
names(df4) <- c("link","date","title","text")

outPath <- "/Users/casy/Dropbox/My_Projects/2015_06_HelpGatov/ data/publications_txt_merged.csv"
write.csv(df4, outPath)
