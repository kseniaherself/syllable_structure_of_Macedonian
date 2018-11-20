library(tidyverse); library(rvest); library('xml2'); library(stringr)

results <- character()

urls <- paste0("http://sgjp.pl/edycja/ajax/inflection-tables/?lexeme_id=",
               1:999999,
               "&variant=1")

sapply(1:length(urls), function(url_n){
  source <- read_html(jsonlite::fromJSON(urls[url_n])$html)
  tag <- unlist(str_extract_all(str_extract(source, 'span class="form p.*?"'), "p[0-9]{1,}"))
  sapply(1:length(tag), function(id){
  source %>% 
    #html_nodes(css = "td") %>%
    html_nodes(css = paste0("span.form.", tag[id])) %>%
    html_text() ->
      result
    results <<- c(results, result)
})})

data_frame(results) %>% 
  write_csv("Desktop/BA_thesis/polish dictionary/polish.csv")

