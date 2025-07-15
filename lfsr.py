def lfsr(init_state, length=15):
    # 将初始状态转换为整数
    state = init_state
    sequence = []
    sequence.append(str(init_state&1))
    state_sequence = []

    for _ in range(length):
        # 保存当前状态
        state_sequence.append(format(state, '04b'))
        # 计算反馈位，根据多项式 g2(x) = x^4 + x^3 + 1
        feedback = ((state >> 3) & 1) ^ ((state>>0) & 1) 
        # 将反馈位加到状态的最低位
        state = (state<< 1 | (feedback)) & 0b1111  # 保持状态为4位
        sequence.append(str(feedback))

    return ''.join(sequence), state_sequence

# 初始状态
init_state = 0b0001
output_sequence, state_sequence = lfsr(init_state)

print("输出序列: ", output_sequence)
print("状态变迁: ")
for i, state in enumerate(state_sequence):
    print(f"{state}",end='->')