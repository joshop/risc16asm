SRCS := $(shell find src -name '*.c')
OBJS := $(SRCS:src/%.c=build/%.o)
CFLAGS := -fsanitize=address -fanalyzer -Wall -Wextra -Werror -g -O3 -I/home/rous/.local/include -fsanitize=undefined -std=c23 -lstc -L/home/rous/.local/lib
LDFLAGS := -fsanitize=address -O3 -fsanitize=undefined -L/home/rous/.local/lib -lstc


build/%.o: src/%.c
	clang-tidy $< --config-file ./.clang-tidy -header-filter="(?!stc.*)" --quiet
	$(CC) -c $(CFLAGS) $< -o $@

build/risc16asm: $(OBJS)
	$(CC) $^ -o build/risc16asm $(LDFLAGS)

clean:
	rm -f build/*.o build/risc16asm
