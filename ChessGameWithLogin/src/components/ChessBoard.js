import React from 'react';
import ChessPiece from './ChessPiece';
import '../styles/ChessBoard.css';

const ChessBoard = ({ board, onPieceClick, onSquareClick }) => {
  const renderSquare = (row, col) => {
    const piece = board[row][col];
    const isLight = (row + col) % 2 === 0;
    const squareClass = isLight ? 'light-square' : 'dark-square';

    const handleClick = () => {
      if (piece) {
        onPieceClick(piece, [row, col]);
      } else {
        onSquareClick([row, col]);
      }
    };

    return (
      <div
        key={`${row}-${col}`}
        className={`chess-square ${squareClass}`}
        onClick={handleClick}
      >
        {piece && (
          <ChessPiece
            piece={piece.name}
            color={piece.color}
            position={[row, col]}
          />
        )}
      </div>
    );
  };

  const renderBoard = () => {
    const squares = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        squares.push(renderSquare(row, col));
      }
    }
    return squares;
  };

  return <div className="chess-board">{renderBoard()}</div>;
};

export default ChessBoard;