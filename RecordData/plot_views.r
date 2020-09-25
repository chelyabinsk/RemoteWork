require(anytime)
require(ggplot2)
require(sqldf)
#library(dplyr)

rm(data)
setwd('H:/pietro/RecordData/viewers/')
#setwd('/home/pirate/Unifolder/pietro/RecordData/viewers')

date <- "2020-09-24"

data <- read.csv(paste(date,".txt",sep=""),sep = "\t",encoding = "UTF-8",quote="")
#data$channel <- data[,1]
data$timestamp <- anytime(data$timestamp)
#data$video <- paste(data$channel,data$video_c)

dd <- data
data <- sqldf('select * from data where live="True"')

ggplot(data) +
  #geom_path(aes(x=timestamp, y=viewers, group=video,color=video)) +
  geom_point(aes(x=timestamp, y=viewers,group=channel_name,color=channel_name)) +
  #geom_path(aes(x=timestamp, y=viewers,group=channel,color=channel)) +
  ggtitle(paste("YouTube Live\n",date,sep="")) +
  theme(plot.title = element_text(hjust = 0.5))


ggplot(data) +
  geom_path(aes(x=timestamp, y=likes/(likes+dislikes), group=video,color=video)) +
  ggtitle(paste("YouTube Live\n",date,sep="")) +
  theme(plot.title = element_text(hjust = 0.5))

plot_diff <- function(da){
  videos <- sqldf('select distinct video from da')
  diff_df <- data[0,]
  for(vid in videos[,1]){
    print(vid)
    d <- sqldf(paste('select distinct * from da where video="',vid,'" order by timestamp',sep=''))
    
    # Calculate the differences
    tmp <- d[-1,2:4] - d[-nrow(d),2:4]
    tmp$timestamp <- d$timestamp[1:length(d$timestamp)-1]
    tmp$video <- vid  
    tmp$channel <- d$channel_name[1:length(d$channel_name)-1]
    
    diff_df<-rbind(diff_df,tmp)
  }
  return(diff_df)
}


change <- plot_diff(data)
change$viewers_delta <- change$viewers
ggplot(change) +
  geom_path(aes(x=timestamp, y=viewers_delta,group=channel,color=channel)) +
  ggtitle(paste("YouTube Live\n",date,sep="")) +
  theme(plot.title = element_text(hjust = 0.5)) 