# Maze Solver AI

Dự án mô phỏng và giải mê cung sử dụng các thuật toán tìm kiếm AI khác nhau. Được phát triển cho môn học Nhập môn Trí tuệ nhân tạo tại Đại học Bách Khoa Hà Nội.

## Tính năng

- Tạo mê cung ngẫu nhiên
- Giải mê cung bằng nhiều thuật toán khác nhau:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A\* Search
  - Greedy Best-First Search (GBFS)
  - Bidirectional BFS
- Hiển thị trực quan quá trình tìm kiếm
- Thống kê hiệu suất của các thuật toán

## Cài đặt

1. Clone repository:

```bash
git clone https://github.com/andrew-taphuc/maze-solver-ai-intro.git
cd maze-solver-ai-intro
```

2. Cài đặt các thư viện cần thiết:

```bash
pip install pygame
```

## Cách sử dụng

1. Chạy chương trình:

```bash
python src/main.py
```

2. Điều khiển:

- Nhấn "GENERATE MAZE" để tạo mê cung mới
- Chọn thuật toán giải mê cung:
  - BFS: Tìm kiếm theo chiều rộng
  - DFS: Tìm kiếm theo chiều sâu
  - A STAR: Thuật toán A\*
  - GBFS: Greedy Best-First Search
  - BIDIRECTIONAL BFS: Tìm kiếm hai chiều

## Cấu trúc dự án

```
maze-solver-ai-intro/
├── src/
│   ├── main.py           # File chính của chương trình
│   ├── cell.py           # Class Cell để biểu diễn ô trong mê cung
│   ├── config.py         # Cấu hình và hằng số
│   ├── utils.py          # Các hàm tiện ích
│   └── search/           # Thư mục chứa các thuật toán tìm kiếm
│       ├── bfs.py
│       ├── dfs.py
│       ├── astar.py
│       ├── gbfs.py
│       └── bidirectionalbfs.py
└── README.md
```

## Công nghệ sử dụng

- Python 3.x
- Pygame
- Các thuật toán tìm kiếm AI

## Tác giả

- Tạ Hồng Phúc ([@andrew-taphuc](https://github.com/andrew-taphuc))
- Nguyễn Mạnh Tùng ([@nmtun](https://github.com/nmtun))
- Bùi Quang Hưng ([@Gnuhq26](https://github.com/Gnuhq26))
- Nguyễn Đức Quang ([@ndquang21](https://github.com/ndquang21))

Sinh viên ngành CNTT Việt - Nhật, Đại học Bách Khoa Hà Nội

## Giấy phép
Dự án này được phát triển cho mục đích học tập và nghiên cứu.
