# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from StockProcessData import ProcessType, process_json_file


class DataViewerApp:
    """
    一个基于Tkinter的图形界面应用，用于浏览指定文件夹下的JSON数据文件，并支持数据显示和K线图展示。
    """

    def __init__(self, root, default_folder=r"E:\stock_json"):
        """
        初始化界面组件，包括文件夹选择、文件列表、数据表格等。
        """
        self.root = root
        self.root.title("数据文件查看器")
        self.root.state("zoomed")  # 窗口默认最大化

        # 文件夹选择行
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5, fill=tk.X)
        self.folder_label = tk.Label(top_frame, text="选择文件夹:")
        self.folder_label.pack(side=tk.LEFT)
        self.folder_button = tk.Button(top_frame, text="选择文件夹", command=self.select_folder)
        self.folder_button.pack(side=tk.LEFT, padx=5)

        # 添加处理类型下拉框
        self.process_type_var = tk.StringVar()
        self.process_type_combobox = ttk.Combobox(
            top_frame,
            textvariable=self.process_type_var,
            state="readonly",
            values=[e.desc for e in ProcessType]
        )
        tk.Label(top_frame, text="处理类型").pack(side=tk.LEFT)
        self.process_type_combobox.current(0)
        self.process_type_combobox.pack(side=tk.LEFT, padx=5)

        # 筛选输入框和按钮
        self.filter_entry = tk.Entry(top_frame, width=20)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_button = tk.Button(top_frame, text="筛选", command=self.filter_files)
        self.filter_button.pack(side=tk.LEFT, padx=5)
        self.show_bi_var = tk.BooleanVar(value=False)
        self.show_zhongshu_var = tk.BooleanVar(value=False)
        self.checkbox_bi = tk.Checkbutton(
            root, text="显示笔与线段", variable=self.show_bi_var)
        self.checkbox_zhongshu = tk.Checkbutton(
            root, text="显示中枢", variable=self.show_zhongshu_var)
        # 绑定处理类型选择事件
        self.process_type_combobox.bind("<<ComboboxSelected>>", self.on_process_type_change)
        # 初始隐藏
        self.checkbox_bi.pack_forget()
        self.checkbox_zhongshu.pack_forget()

        # 文件列表框
        self.file_listbox = tk.Listbox(root, width=80, height=10)
        self.file_listbox.pack(pady=10)
        self.file_listbox.bind("<<ListboxSelect>>", self.display_file_data)

        # 数据表格（Treeview）
        self.tree = ttk.Treeview(root, columns=[], show="headings")
        self.tree.pack(expand=True, fill="both", pady=10)
        self.tree.bind("<Double-1>", self.show_kline_chart)  # 双击数据行显示K线图

        # 默认文件夹路径
        self.folder_path = default_folder
        self.all_files = []  # 保存所有文件名
        # 启动时自动选择文件夹
        if os.path.exists(self.folder_path):
            self.load_value_json_files()
        else:
            messagebox.showwarning("警告", f"默认文件夹不存在: {self.folder_path}")

    def select_folder(self):
        """
        弹出文件夹选择对话框，选择后加载该文件夹下的JSON文件列表。
        """
        path = filedialog.askdirectory(initialdir=self.folder_path)
        if not path:
            path = self.folder_path  # 用户取消选择时，使用默认路径
        if not os.path.exists(path) or not os.path.isdir(path):
            messagebox.showerror("错误", f"路径不存在: {path}")
            return
        self.folder_path = path
        self.load_value_json_files()
        if not self.all_files:
            messagebox.showerror("错误", f"文件夹内没有合法的JSON文件: {self.folder_path}")

    def on_process_type_change(self, event=None):
        desc = self.process_type_var.get()
        if desc == "缠中论禅":
            self.checkbox_bi.pack(pady=2)
            self.checkbox_zhongshu.pack(pady=2)
        else:
            self.checkbox_bi.pack_forget()
            self.checkbox_zhongshu.pack_forget()

    def load_value_json_files(self):
        self.file_listbox.delete(0, tk.END)
        self.all_files = [file for file in os.listdir(self.folder_path) if
                          file.endswith(".json")]
        for file in self.all_files:
            self.file_listbox.insert(tk.END, file)

    def display_file_data(self, event):
        """
        当用户选择文件时，读取JSON文件内容并显示在数据表格中。
        """
        selected_file_index = self.file_listbox.curselection()
        if not selected_file_index:
            return
        selected_file = self.file_listbox.get(selected_file_index)
        file_path = os.path.join(self.folder_path, selected_file)

        try:
            # 获取选中的ProcessType
            process_type_desc = self.process_type_var.get()
            process_type = next((e for e in ProcessType if e.desc == process_type_desc), ProcessType.NO_PROCESS)
            df = process_json_file(file_path, process_type)

            # 清空旧数据
            for col in self.tree["columns"]:
                self.tree.heading(col, text="")
            self.tree.delete(*self.tree.get_children())

            # 设置新列
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)

            # 插入数据行
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.current_data = df  # 保存当前数据

            # 只对“持仓量”及之前的字段自适应宽度
            columns = list(df.columns)
            last_idx = 13
            font = ("微软雅黑", 10)
            for idx, col in enumerate(columns):
                if idx <= last_idx:
                    max_width = max(
                        [len(str(col))] +
                        [len(str(row[col])) for _, row in df.iterrows()]
                    )
                    pixel_width = max_width * 10 + 20
                    self.tree.column(col, width=pixel_width)
                else:
                    self.tree.column(col, width=100)  # 后续字段宽度固定
        except Exception as e:
            messagebox.showerror("错误", f"无法加载文件: {e}")

    def filter_files(self):
        keyword = self.filter_entry.get().strip()
        self.file_listbox.delete(0, tk.END)
        for file in self.all_files:
            if keyword in file:
                self.file_listbox.insert(tk.END, file)

    def show_kline_chart(self, event):
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        selected_item = self.tree.selection()
        if not selected_item:
            return

        df = getattr(self, "current_data", None)
        if df is None or df.empty:
            messagebox.showerror("错误", "数据为空")
            return

        try:
            desc = self.process_type_var.get()
            kline_window = tk.Toplevel(self.root)
            kline_window.state("zoomed")  # 新增：窗口最大化
            if desc == "缠中论禅":
                kline_window.title("缠中论禅K线图")
            else:
                kline_window.title(f"K线图")
            kline_window.geometry("1000x450")

            n = len(df)
            base_width = 12
            if n > 20:
                fig_width = n * 0.22
            else:
                fig_width = base_width

            fig, (ax_k, ax_pos) = plt.subplots(
                2, 1, figsize=(fig_width, 8), gridspec_kw={'height_ratios': [4, 1]},
                sharex=True
            )

            x = range(n)
            show_bi = desc == "缠中论禅" and self.show_bi_var.get()
            for i, row in enumerate(df.itertuples()):
                open_price = float(getattr(row, "开盘价"))
                close_price = float(getattr(row, "收盘价"))
                high_price = float(getattr(row, "最高价"))
                low_price = float(getattr(row, "最低价"))
                if desc == "缠中论禅":
                    rect_color = "Goldenrod"
                else:
                    rect_color = "red" if close_price > open_price else "green"
                ax_k.add_patch(
                    mpatches.Rectangle(
                        (i - 0.2, min(open_price, close_price)), 0.4,
                        abs(close_price - open_price),
                        color=rect_color, zorder=2
                    )
                )
                ax_k.scatter(i - 0.001, high_price, color=rect_color, s=1.01, zorder=3)
                ax_k.scatter(i - 0.001, low_price, color=rect_color, s=1.01, zorder=3)
                ax_k.add_patch(
                    mpatches.Rectangle(
                        (i - 0.04, low_price), 0.08, high_price - low_price,
                        color=rect_color, zorder=1
                    )
                )
                # 新增：绘制顶底分型标记
                if show_bi and "顶底分型" in df.columns:
                    fenxing = getattr(row, "顶底分型", None)
                    if fenxing is not None:
                        # 兼容枚举和字符串
                        fx_val = str(fenxing)
                        if "TOP" in fx_val or "顶分型" in fx_val:
                            # 顶分型，顶部画红色小矩形
                            ax_k.add_patch(
                                mpatches.Rectangle(
                                    (i - 0.12, high_price + (high_price - low_price) * 0.03),
                                    0.24, (high_price - low_price) * 0.06,
                                    color="red", zorder=5
                                )
                            )
                        elif "BOTTOM" in fx_val or "底分型" in fx_val:
                            # 底分型，底部画绿色小矩形
                            ax_k.add_patch(
                                mpatches.Rectangle(
                                    (i - 0.12, low_price - (high_price - low_price) * 0.09),
                                    0.24, (high_price - low_price) * 0.06,
                                    color="green", zorder=5
                                )
                            )
            ax_k.set_title(f"K线图")
            ax_k.set_ylabel("价格")
            ax_k.set_xlim(-0.5, n - 0.5)
            ax_k.grid(axis="y")

            # 右侧价格刻度
            ax_k_right = ax_k.twinx()
            ax_k_right.set_ylim(ax_k.get_ylim())
            ax_k_right.set_yticks(ax_k.get_yticks())
            ax_k_right.set_ylabel("价格", rotation=270, labelpad=15)
            ax_k_right.yaxis.set_label_position("right")
            ax_k_right.yaxis.set_ticks_position("right")
            ax_k_right.tick_params(axis="y", direction="in", pad=2)
            ax_k_right.grid(False)

            if "成交量" in df.columns and "持仓量" in df.columns:
                volume = df["成交量"].astype(float).values
                position = df["持仓量"].astype(float).values
                ax_pos.bar(x, volume, color="#888888", width=0.6, alpha=0.6, label="成交量")
                ax_pos.plot(x, position, color="blue", marker="o", markersize=5, label="持仓量")
                ax_pos.set_ylabel("成交/持仓")
                ax_pos.legend(loc="upper left", fontsize=8)
                ax_pos.grid(axis="y")
                # 右侧持仓量刻度
                ax_pos_right = ax_pos.twinx()
                ax_pos_right.set_ylim(ax_pos.get_ylim())
                ax_pos_right.set_yticks(ax_pos.get_yticks())
                ax_pos_right.set_ylabel("成交/持仓", rotation=270, labelpad=15)
                ax_pos_right.yaxis.set_label_position("right")
                ax_pos_right.yaxis.set_ticks_position("right")
                ax_pos_right.tick_params(axis="y", direction="in", pad=2)
                ax_pos_right.grid(False)
            else:
                ax_pos.text(0.5, 0.5, "无成交量/持仓量数据", ha="center", va="center", fontsize=12)

            if "日期" in df.columns:
                ax_pos.set_xticks(list(x))
                ax_pos.set_xticklabels(df["日期"], rotation=45, fontsize=8)

            canvas_frame = tk.Frame(kline_window)
            canvas_frame.pack(fill=tk.BOTH, expand=True)
            canvas = tk.Canvas(canvas_frame, width=1000, height=800, bg="white")
            canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            fig_canvas = FigureCanvasTkAgg(fig, master=canvas)
            fig_canvas.draw()
            fig_widget = fig_canvas.get_tk_widget()
            fig_widget.update_idletasks()
            widget_width = max(fig_widget.winfo_reqwidth(), 1000)
            canvas.create_window((0, 0), window=fig_widget, anchor="nw")
            canvas.config(scrollregion=(0, 0, widget_width, 800))

            def on_press(event):
                canvas.scan_mark(event.x, event.y)

            def on_drag(event):
                canvas.scan_dragto(event.x, event.y, gain=1)

            canvas.bind("<ButtonPress-1>", on_press)
            canvas.bind("<B1-Motion>", on_drag)

            # 左上角按钮
            btn_frame = tk.Frame(canvas_frame, bg="white")
            btn_frame.place(x=10, y=10)

            def move_left():
                canvas.xview_scroll(-1, "units")

            def move_right():
                canvas.xview_scroll(1, "units")

            btn_left = tk.Button(btn_frame, text="←", width=3, command=move_left)
            btn_left.pack(side=tk.LEFT, padx=2)
            btn_right = tk.Button(btn_frame, text="→", width=3, command=move_right)
            btn_right.pack(side=tk.LEFT, padx=2)

            def on_chart_double_click(event):
                # 获取鼠标在画布上的像素坐标
                x_pixel = event.x
                y_pixel = event.y
                # 将像素坐标转换为matplotlib坐标
                inv = fig.transFigure.inverted()
                x_fig, y_fig = inv.transform((x_pixel, y_pixel))
                # 转换为数据坐标
                ax_x = ax_k.transData.inverted()
                try:
                    xdata, _ = ax_x.transform((x_pixel, y_pixel))
                except Exception:
                    return
                idx = int(round(xdata))
                if idx < 0 or idx >= len(df):
                    return
                row = df.iloc[idx]
                info = []
                for col in ["日期", "最高价", "最低价", "开盘价", "收盘价", "持仓量", "成交量"]:
                    if col in row:
                        info.append(f"{col}: {row[col]}")
                info_text = "\n".join(info)

                # 创建悬浮窗
                tooltip = tk.Toplevel(kline_window)
                tooltip.wm_overrideredirect(True)  # 无边框
                tooltip.attributes("-topmost", True)
                label = tk.Label(tooltip, text=info_text, bg="#ffffe0", relief="solid", borderwidth=1,
                                 font=("微软雅黑", 10))
                label.pack(ipadx=8, ipady=4)
                # 计算悬浮窗位置（相对于主窗口）
                abs_x = kline_window.winfo_rootx() + 10
                abs_y = kline_window.winfo_rooty() + 10
                tooltip.wm_geometry(f"+{abs_x + 10}+{abs_y + 10}")

                # 鼠标移开或5秒后自动销毁
                def close_tooltip(_=None):
                    if tooltip.winfo_exists():
                        tooltip.destroy()

                label.bind("<Leave>", close_tooltip)
                tooltip.after(10000, close_tooltip)

            fig_widget.bind("<Double-1>", on_chart_double_click)
        except Exception as e:
            messagebox.showerror("错误", f"无法生成K线图: {e}")


if __name__ == "__main__":
    # 启动主程序
    root = tk.Tk()
    app = DataViewerApp(root, r"E:\stock_json")
    root.mainloop()
