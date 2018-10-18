library(tidyverse)
expand.grid(c("O", "OO", "OOO", "OS", "OOS", "OSS", "SS", "S"), c("S", "SS", "SO", "SSO", "SOO", "OOO", "OO", "O")) %>% 
  mutate(result = paste0(Var1,"V", Var2)) %>% 
  select(result) %>% 
  write_csv("all_possible_syllables.csv")

