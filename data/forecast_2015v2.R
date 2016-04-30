library(forecast)

data <- read.table("/Users/phil/taxi-news/data/r_data_v2.csv", header = TRUE, sep = ",")
data <- data[,1:8]

news_day     = 539 #174
next_day     = news_day + 1
look_back    = 120 #120
look_forward = 30

week_count = 0
week_label = c()
labels = lapply(data[,1],as.character)
for(i in (news_day - look_back):(next_day + look_forward)){
  if (i%%7 == 1) {
    week_label = c(week_label,labels[i])
    week_count = week_count + 1
  }
}

X <- data[(news_day-look_back):news_day,3:8]
X2 <- data[next_day:(next_day+look_forward),3:8]

df <- data[(news_day-look_back):news_day,]
y <- ts(df['count'],frequency=7)
y2 <- ts(data[(news_day-look_back):(next_day+look_forward),2],frequency=7)

# Forecast using ETS method 
fc.ets = forecast(y)
plot(fc.ets)
plot(fc.ets$residuals)
plot(fc.ets$fitted)

# Forecast using ARIMA method
ar = auto.arima(y,xreg=X)
fc.arima = forecast(ar,xreg=X2)
plot(fc.arima,main="Forecasted Daily Yellow Cab Rides", xlab="Date", ylab="Trips", xaxt="n", col="black",lwd=.5)
axis(1,at=c(1:22),labels=week_label)
lines(fc.arima$fitted,col="blue",lwd=1.5)
lines(y2,col="red",lwd=1)
legend("bottomleft", legend=c("actual rides in red"), text.col='red')

# Compare accuracy
accuracy(fc.ets)
accuracy(fc.arima)
summary(ar)
