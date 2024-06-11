import React from 'react';

const ChessPiece = ({ piece, color, position }) => {
  const pieceImageMap = {
    Pawn: 'pawn',
    Knight: 'knight',
    Bishop: 'bishop',
    Rook: 'rook',
    Queen: 'queen',
    King: 'king',
  };

  const pieceImage = pieceImageMap[piece];
  const pieceColor = color === 'white' ? 'w' : 'b';
  const imageSrc = `./assets/pieces/${pieceColor}${pieceImage}.png`;
  const altText = `${color} ${piece}`;

  const handleDragStart = (e) => {
    e.dataTransfer.setData('piece', JSON.stringify({ piece, color, position }));
  };

  return (
    <img
      src={imageSrc}
      alt={altText}
      className="chess-piece"
      draggable
      onDragStart={handleDragStart}
    />
  );
};

export default ChessPiece;