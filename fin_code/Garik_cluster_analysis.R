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
  filter(n_sylables>1) %>% 
  select(-n_sylables) ->
  df

write_csv(df[FALSE, ], "clusters.csv")

sapply(1:nrow(df), function(i){
  result <- data_frame(
    lemma = df$lemma[i],
    mac = df$mac[i],
    cluster = unlist(str_split(df$mac[i], "V")),
    id = df$id[i],
    cl_id = 1:length(unlist(str_split(df$mac[i], "V")))
  )
  write_csv(result, "clusters.csv", append = TRUE)
})

read_csv("clusters.csv") %>% 
  mutate(predicted = str_detect(cluster, "(SO|SS|OO|S|O)?O?O?(OS|SS|OO|S|O)?")) %>%
  count(predicted)
