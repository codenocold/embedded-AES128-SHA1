#include <stdio.h>
#include "sha1.h"


static inline void dump(const char *label, const uint8_t *buf, size_t len)
{
  printf("%s: ", label);
  for (size_t i = 0; i < len; i++)
    printf("%02x", buf[i]);
  printf("\n");
}


int main(void)
{
  const cf_chash *hash = &cf_sha1;
  const uint8_t msg[] = "123456";
  uint8_t digest[20];

  cf_chash_ctx ctx;
  hash->init(&ctx);

  hash->update(&ctx, msg, sizeof(msg)-1);
  hash->digest(&ctx, digest);

  dump("plaintext", msg, sizeof(msg)-1);
  dump("SHA1", digest, sizeof(digest));  

  return 0;
}
