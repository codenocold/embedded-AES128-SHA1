#include <stdio.h>
#include "aes.h"


static inline void dump(const char *label, const uint8_t *buf, size_t len)
{
  printf("%s: ", label);
  for (size_t i = 0; i < len; i++)
    printf("%02x", buf[i]);
  printf("\n");
}


int main(void)
{
  uint8_t key[]   =  "1234567890123456";
  uint8_t plainmsg[] =  "1234567890123456";
  uint8_t ciphermsg[16];

  cf_aes_context ctx;
  cf_aes_init(&ctx, key, sizeof(key)-1);

  printf("ENCRYPT\n");
  dump("\tplaintext ", plainmsg, 16);
  cf_aes_encrypt(&ctx, plainmsg, ciphermsg);
  dump("\tciphertext", ciphermsg, 16);

  printf("DECRYPT\n");
  dump("\tciphertext", ciphermsg, 16);
  cf_aes_decrypt(&ctx, ciphermsg, plainmsg);
  dump("\tplaintext ", plainmsg, 16);

  cf_aes_finish(&ctx);

  return 0;
}