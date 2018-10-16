setwd("/home/agricolamz/for_work/HSE/students/2017-2018_b3_Romanova/fin_code")
df <- read_tsv("phon_table.tsv")
df <- df[,c("lemma", "quality_lettering")]
colnames(df)[2] <- "mac"

df %>% 
  mutate(n_sylables = str_count(mac, "V"),
         mac = str_replace_all(mac, "-", ""),
         cluster = NA,
         id = 1:nrow(df),
         cl_id = NA) %>% 
  filter(n_sylables>1) ->
  df

final <- df[FALSE, ]

sapply(1:nrow(df), function(i){
  result <- data_frame(
    id = df$id[i],
    lemma = df$lemma[i],
    mac = df$mac[i],
    cluster = unlist(str_extract_all(df$mac[i], "VS*?O*?S*?V")),
    cl_id = 1:length(unlist(str_extract_all(df$mac[i], "VS*?O*?S*?V")))
  )
  final <<- rbind(final, result)
})

final %>% 
  mutate(predicted = str_detect(cluster, "V(SO|SS|OO|S|O)?O?O?(OS|SS|OO|S|O)?V"))
