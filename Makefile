CFLAGS += -g -O0 -std=gnu99 -fPIC -Wall -Wextra -Werror \
	  -Wno-unused-parameter -Wno-missing-field-initializers

TARGETS = test_aes128 test_sha1
all: $(TARGETS)

SOURCES = aes.o sha1.o chash.o blockwise.o

test_aes128: $(SOURCES) test_aes128.o
test_sha1: $(SOURCES) test_sha1.o

clean:
	rm -f *.o test_sha1 test_aes128
