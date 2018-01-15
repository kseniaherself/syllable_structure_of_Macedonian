library(tidyverse); library(rvest)

source <- read_html("http://www.makedonski.info/letter/%D1%84")

source %>% 
  html_nodes("#ranges > select:nth-child(1)") %>%
  html_text() -> 
  titles

two_titles <- unlist(str_split(titles, "\n\t  \n\t    "))
source2 <- paste0("http://www.makedonski.info/letter/ф/",
       unlist(str_split(two_titles[1], " - "))[1],
       "/",
       unlist(str_split(two_titles[1], " - "))[2],
       "/",
       collapse = "")

source2 <- read_html(source2)

source2 %>% 
  html_nodes("#ranges > select:nth-child(1)") %>%
  html_text() -> 
  titles

#lexems > select:nth-child(1) > option:nth-child(1)
#lexems > select:nth-child(1) > option:nth-child(2)