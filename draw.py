import matplotlib.pyplot as plt
import numpy as np

# 1. 载入您的原始数据
base = np.array([40.25, 23.00, 34.00, 25.73, 86.00, 23.40, 39.42])

data_ratio_raw = {
    "OmniGen2(GtA)":     np.array([41.25, 13.00, 41.50, 21.91, 79.00, 26.40, 34.52]) / base,
    "UniWorld-V1(GtA)":  np.array([24.00, 19.00, 34.50, 24.72, 80.00, 24.80, 39.35]) / base,
    "OneCAT-3b(GtA)":    np.array([33.50,  8.50, 29.00, 20.69, 74.00, 23.80, 33.10]) / base,
    "uni-video(GtA)":    np.array([34.00, 21.50, 29.00, 29.33, 61.00, 20.00, 42.76]) / base,
    "UniPic2(GtA)":      np.array([17.50, 17.00, 31.00, 23.95, 47.00, 24.60, 38.80]) / base,
    "STAR-7B(GtA)":      np.array([34.00, 14.50, 32.50, 23.56, 79.00, 25.20, 38.56]) / base,
}

labels_raw = [
    "Real-world\nApps",
    "Math\nReasoning",
    "STEM",
    "Puzzles\n& Games",
    "Chart",
    "Spatial\nIntel.",
    "Perception\nReasoning",
]

# 2. 重新排序：确保 STEM 在正上方，并按原图顺时针排列
# 原始索引对应的标签：2:STEM, 1:Math, 0:Real-world, 6:Perception, 5:Spatial, 4:Chart, 3:Puzzles
order = [2, 1, 0, 6, 5, 4, 3]
labels = [labels_raw[i] for i in order]
data_ratio = {k: v[order] for k, v in data_ratio_raw.items()}

# 计算角度
N = len(labels)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # 闭合圆环

# 3. 创建图表 & 基础美化
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

# 设定图表背景颜色，带来柔和现代感
bg_color = '#f8f9fc'
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 调整旋转方向
ax.set_theta_offset(np.pi / 2)  # 让起始位置在正上方
ax.set_theta_direction(-1)      # 顺时针绘制

# 4. 坐标轴与网格线
plt.xticks(angles[:-1], labels, size=11)
ax.set_rlabel_position(22)      # 调整数值标签的位置，防遮挡
plt.yticks([0.50, 0.75, 1.00, 1.25], ["0.50", "0.75", "1.00", "1.25"], color="#333333", size=10)
plt.ylim(0, 1.25)               # 您设定的 max radius 1.25

# 柔化内部网格，加粗着色外圈
ax.grid(color='#dcdcdc', linestyle='-', linewidth=1)
ax.spines['polar'].set_color('#cdd4e6')
ax.spines['polar'].set_linewidth(3)

# 绘制 1.0 基准虚线多边形
ax.plot(angles, [1.0]*len(angles), linewidth=1.5, linestyle='--', color='tab:blue', alpha=0.9, label='_nolegend_')

# 5. 遍历并绘制各模型的数据线
colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

for idx, (label, values) in enumerate(data_ratio.items()):
    values_closed = np.concatenate((values, [values[0]]))
    color = colors[idx]
    
    # 画中心实线
    ax.plot(angles, values_closed, linewidth=2, linestyle='solid', label=label, color=color)
    
    # 叠加一层半透明粗线，模拟一点“发光光晕”的效果
    ax.plot(angles, values_closed, linewidth=6, linestyle='solid', color=color, alpha=0.15)
    
    # 区域半透明填充
    ax.fill(angles, values_closed, color=color, alpha=0.08)

# 6. 图例和标题收尾
plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), frameon=False, fontsize=11)
plt.title('Relative Performance to Base (GtA only, max=1.25)', size=15, y=1.1, weight='bold', color='#222222')

plt.tight_layout()
plt.savefig('radar_chart.png', dpi=300, bbox_inches='tight')
plt.show()