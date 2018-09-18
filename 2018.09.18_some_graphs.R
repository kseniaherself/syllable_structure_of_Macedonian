setwd("/home/agricolamz/for_work/HSE/students/2017-2018_b3_Romanova")
library(tidyverse)
library(ggrepel)
finals <- read_tsv("fin_code/finals_freq.txt", col_names = FALSE)
finals %>% 
  mutate(n_sounds = str_count(X1, "-")+1) %>% 
  arrange(n_sounds) %>% 
  mutate(id = 1:nrow(finals)) %>% 
  ggplot(aes(id, X2, label = X1))+
  geom_label_repel()+
  scale_y_log10()+
  theme_bw()+
  facet_wrap(~n_sounds, scales = "free")

initials <- read_tsv("fin_code/initials_freq.txt", col_names = FALSE)
initials %>% 
  mutate(n_sounds = str_count(X1, "-")+1) %>% 
  arrange(n_sounds) %>% 
  mutate(id = 1:nrow(initials)) %>% 
  ggplot(aes(id, X2, label = X1))+
  geom_label_repel()+
  scale_y_log10()+
  theme_bw()+
  facet_wrap(~n_sounds, scales = "free")

phoible <- read_csv("phoible.csv")

initials %>% 
  mutate(n_sounds = str_count(X1, "-")+1) %>% 
  filter(n_sounds == 1) %>% 
  left_join(phoible, by = c("X1" = "name")) %>% 
  filter(!is.na(frequency)) %>% 
  summarise(cor = cor(X2, frequency, method = "spearman"))

finals %>% 
  mutate(n_sounds = str_count(X1, "-")+1) %>% 
  filter(n_sounds == 1) %>% 
  left_join(phoible, by = c("X1" = "name")) %>% 
  filter(!is.na(frequency)) %>% 
  summarise(cor = cor(X2, frequency, method = "spearman"))

finals$part_of_syllable <-  "finals"
initials$part_of_syllable <-  "initials"
rbind(initials, finals) %>% 
  spread(part_of_syllable, X2, fill = 0) %>% 
  ggplot(aes(finals, initials, label = X1))+
  geom_abline(slope = 1, intercept = 0, linetype= 2)+
  geom_text()+
  scale_x_log10()+
  scale_y_log10()+
  theme_bw()
