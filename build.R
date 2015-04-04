#
#   build.R: build congressional education dataset 
#

# directory names
data.path     <- "data"
raw.data	<-"sessions" 
header.fn <- "header.csv"
out.fn <- "congress_edu.csv"

dir_fifo = c()

pushd <- function(cd) {
	# usage: pushd("directory to change to")
	dir_fifo = append(dir_fifo, getwd(), 0)
	assign("dir_fifo", dir_fifo, envir = .GlobalEnv)
	setwd(cd)
}

popd <- function() {
	# usage: popd()
	setwd(dir_fifo[1])
	dir_fifo = dir_fifo[-1]
	assign("dir_fifo", dir_fifo, envir = .GlobalEnv)
}

read.headers <- function() {
	## Read in header files and define global variables
	header <- "header.csv"
	# set global header file frames
	header <<- read.csv("header.csv", header = FALSE)
}

read.data <- function(session_num) {
	pushd(raw.data)
	# read individual contribution file
	data.fn <- paste("bios_", session_num, ".csv", sep="")
	data <- read.table(file = data.fn, header = FALSE, sep = ",")
	popd()
	return(data)
}

read.rec <- function(session_num) {
	# recursively merge all data files up until sessions session_num
	add <- read.data(session_num)
	if (session_num == 90) {
		return(header)
	}
	else {
		old <- read.rec(session_num - 1)
		new <- rbind(old, add)
		return(new)
	}
}

read.all <- function() {
	data <- read.rec(114)
	write.csv(data, out.fn)
}


pushd(data.path)
read.headers()
read.all()
popd()
