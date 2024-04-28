import streamlit as st
import queens as q
import matplotlib.pyplot as plt
import numpy as np


def plot_chessboard(n, queens_positions):
    board = np.zeros((n, n))
    for i in range(n):
        for j in range(i % 2, n, 2):
            board[i][j] = 1
            
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('gray')
    ax.imshow(board, cmap=cmap, interpolation='nearest')

    # Placing queens on the board
    for pos in queens_positions:
        row = (pos - 1) // n
        col = (pos - 1) % n
        ax.text(col, row, '♕', fontsize=18, ha='center', va='center', color='red')

    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig, ax)

st.title("N-Queens")

n = st.selectbox("Select the number of queens.",
                        (3,4,5,6,7,8,9,10), index=None,
                        placeholder="Choose an option")
filename = None
cnf_file_content = None
if n is not None:
    filename,cnf_file_content = q.queens(n)
    st.write(f"DIMACS file {filename} created.")
    text_area_value = st.text_area("File Content", value=cnf_file_content, height=300)

if n is not None:
    st.header("Solution")

if filename is not None:
    result = q.run_minisat(filename)
    st.text(result)
    positions, n = q.create_assignment_array()
    if len(positions) != 0:
        st.subheader("Chess Board")
        plot_chessboard(n, positions)