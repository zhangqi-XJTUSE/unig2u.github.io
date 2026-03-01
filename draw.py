import matplotlib.pyplot as plt
import numpy as np

# ================= 1. 数据准备 =================
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
    "Real-world\nApps", "Math\nReasoning", "STEM", "Puzzles\n& Games",
    "Chart", "Spatial\nIntel.", "Perception\nReasoning",
]

# 排序：STEM在正上方，按顺时针排列
order = [2, 1, 0, 6, 5, 4, 3] 
labels = [labels_raw[i] for i in order]
data_ratio = {k: v[order] for k, v in data_ratio_raw.items()}

N = len(labels)
plot_angles = [n / float(N) * 2 * np.pi for n in range(N)]
tick_angles = plot_angles.copy()
plot_angles += plot_angles[:1]  # 闭合线条

# ================= 2. 画布与底图设置 =================
fig, ax = plt.subplots(figsize=(11, 9), subplot_kw=dict(polar=True))

# 背景色：为了让白色光晕明显，背景需要稍微带一点灰蓝色
bg_color = '#eff2f7'
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.set_theta_offset(np.pi / 2)  
ax.set_theta_direction(-1)      

# 关闭 matplotlib 所有的默认网格和边框，我们自己画！
ax.axis('off')
ax.set_ylim(0, 1.45)

# ================= 3. 纯手工绘制：圈内的线 =================
grid_color = '#d1d6e3'
theta_circle = np.linspace(0, 2*np.pi, 200)

# 3.1 画同心圆 (0.5, 0.75, 1.0)
for r_val in [0.5, 0.75, 1.0]:
    ax.plot(theta_circle, [r_val]*200, color=grid_color, linewidth=1, zorder=1)

# 3.2 画从中心发出的辐射线 (Spokes)
for ang in tick_angles:
    ax.plot([ang, ang], [0, 1.25], color=grid_color, linewidth=1, zorder=1)

# 3.3 画数值刻度标签 (带底色遮罩，防线穿透)
label_angle = tick_angles[1] / 2  # 放置在第一个和第二个轴的中间
for r_val in [0.5, 0.75, 1.0, 1.25]:
    ax.text(label_angle, r_val, f"{r_val:.2f}", color='#555555', size=10, 
            ha='center', va='center', zorder=5,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=bg_color, edgecolor='none', alpha=0.9))

# ================= 4. 纯手工绘制：发光的最外圈 =================
# 在 r=1.25 处叠加 4 层线来模拟真实的 Glow 效果
glow_color = '#a0c4ff' # 浅蓝色光晕
ax.plot(theta_circle, [1.25]*200, color=glow_color, linewidth=20, alpha=0.15, zorder=2) # 最外层大光晕
ax.plot(theta_circle, [1.25]*200, color=glow_color, linewidth=10, alpha=0.30, zorder=2) # 中层过渡光
ax.plot(theta_circle, [1.25]*200, color='#ffffff',  linewidth=5,  alpha=0.80, zorder=2) # 内层白光
ax.plot(theta_circle, [1.25]*200, color='#ffffff',  linewidth=2,  alpha=1.00, zorder=2) # 核心白线

# ================= 5. 绘制多边形虚线基准 (Baseline 1.0) =================
# 【修改处】添加了 label 用于显示在图例中
ax.plot(plot_angles, [1.0]*len(plot_angles), color='tab:blue', linewidth=1.5, linestyle='--', zorder=4, label='Qwen2.5-7b')

# ================= 6. 绘制各模型的数据线 =================
colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

for idx, (label, values) in enumerate(data_ratio.items()):
    values_closed = np.concatenate((values, [values[0]]))
    color = colors[idx]
    
    # 填充
    ax.fill(plot_angles, values_closed, color=color, alpha=0.08, zorder=idx+5)
    # 线条发光
    ax.plot(plot_angles, values_closed, linewidth=6, linestyle='solid', color=color, alpha=0.15, zorder=idx+6)
    # 核心线条
    ax.plot(plot_angles, values_closed, linewidth=2, linestyle='solid', label=label, color=color, zorder=idx+7)

# ================= 7. 绘制外围的文字标签 =================
r_labels = 1.35
for angle, label in zip(tick_angles, labels):
    if label == "STEM":
        ha, va = 'center', 'bottom'
    elif angle > 0 and angle < np.pi / 2: 
        ha, va = 'left', 'bottom'
    elif label == "Real-world\nApps": 
        ha, va = 'left', 'center'
    elif angle > np.pi / 2 and angle < np.pi: 
        ha, va = 'left', 'top'
    elif angle > np.pi and angle < 3 * np.pi / 2: 
        ha, va = 'right', 'top'
    elif label == "Chart": 
        ha, va = 'right', 'center'
    elif angle > 3 * np.pi / 2: 
        ha, va = 'right', 'bottom'
    else:
        ha, va = 'center', 'center'

    ax.text(angle, r_labels, label, size=11, ha=ha, va=va, linespacing=1.2, color='#222222', zorder=10)

# ================= 8. 收尾工作 =================
# 【修改处】微调 bbox_to_anchor 的 X 坐标，给图例留出更多空间
plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), frameon=False, fontsize=11)
plt.title('Model Performance Radar Chart', size=16, y=1.1, weight='bold', color='#222222')

plt.tight_layout()
plt.savefig('radar_chart_pro.png', dpi=300, bbox_inches='tight')
plt.show()