from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import AutoModelForPreTraining  # Or BertForPreTraining for loading pretraining heads
from transformers import AutoModel  # or BertModel, for BERT without pretraining heads
  
model = AutoModelForPreTraining.from_pretrained('raquelsilveira/legalbertpt_fp')
tokenizer = AutoTokenizer.from_pretrained('raquelsilveira/legalbertpt_fp')
