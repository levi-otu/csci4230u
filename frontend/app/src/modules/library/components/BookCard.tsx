/**
 * BookCard Component
 * Displays a book in the user's library with cover, details, and actions
 */

import React from 'react';
import { BookOpen, Heart, Star } from 'lucide-react';
import { Card, CardContent } from '@/global/components/ui/card';
import { Badge } from '@/global/components/ui/badge';
import type { UserBook } from '@/global/models/library.models';

interface BookCardProps {
  userBook: UserBook;
  viewMode: 'grid' | 'list';
  onClick: () => void;
}

/**
 * BookCard Component
 */
export const BookCard: React.FC<BookCardProps> = ({ userBook, viewMode, onClick }) => {
  const { book, reading_status, is_favorite, rating } = userBook;

  if (!book) return null;

  // Render stars for rating
  const renderStars = (rating: number | null) => {
    if (!rating) return null;

    return (
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`h-3 w-3 ${
              star <= rating
                ? 'fill-amber-400 text-amber-400'
                : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    );
  };

  // Grid view
  if (viewMode === 'grid') {
    return (
      <Card
        className="group cursor-pointer overflow-hidden hover:shadow-xl transition-all duration-300 bg-card border-border hover:border-amber-500/50"
        onClick={onClick}
      >
        <CardContent className="p-0">
          {/* Book Cover */}
          <div className="relative aspect-[2/3] bg-gradient-to-br from-amber-100 to-orange-100 overflow-hidden">
            {book.cover_image_url ? (
              <img
                src={book.cover_image_url}
                alt={book.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <BookOpen className="h-16 w-16 text-amber-300" />
              </div>
            )}

            {/* Favorite Badge */}
            {is_favorite && (
              <div className="absolute top-2 right-2 bg-red-500 rounded-full p-1.5 shadow-lg">
                <Heart className="h-4 w-4 text-white fill-white" />
              </div>
            )}

            {/* Status Badge - Unread, Reading, or Finished */}
            {reading_status === 'finished' ? (
              <div className="absolute top-2 left-2">
                <Badge className="bg-green-500 text-white shadow-lg">
                  Read
                </Badge>
              </div>
            ) : reading_status === 'reading' ? (
              <div className="absolute top-2 left-2">
                <Badge className="bg-blue-500 text-white shadow-lg">
                  Reading
                </Badge>
              </div>
            ) : null}
          </div>

          {/* Book Info */}
          <div className="p-4 space-y-2">
            <h3 className="font-semibold text-sm line-clamp-2 min-h-[2.5rem] group-hover:text-amber-600 transition-colors">
              {book.title}
            </h3>
            {book.series_title && (
              <p className="text-xs text-amber-600 dark:text-amber-400 line-clamp-1">
                {book.series_title} {book.volume_number && `Vol. ${book.volume_number}`}
              </p>
            )}
            <p className="text-xs text-muted-foreground line-clamp-1">
              {book.author}
            </p>

            {/* Rating */}
            {rating && (
              <div className="flex items-center gap-2">
                {renderStars(rating)}
                <span className="text-xs text-muted-foreground">
                  {rating.toFixed(1)}
                </span>
              </div>
            )}

            {/* Genre */}
            {book.genre && (
              <Badge variant="outline" className="text-xs">
                {book.genre}
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  // List view
  return (
    <Card
      className="group cursor-pointer hover:shadow-lg transition-all duration-300 bg-card border-border hover:border-amber-500/50"
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex gap-4">
          {/* Book Cover - Smaller in list view */}
          <div className="relative w-24 aspect-[2/3] bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg overflow-hidden flex-shrink-0">
            {book.cover_image_url ? (
              <img
                src={book.cover_image_url}
                alt={book.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <BookOpen className="h-8 w-8 text-amber-300" />
              </div>
            )}

            {/* Favorite Badge */}
            {is_favorite && (
              <div className="absolute top-1 right-1 bg-red-500 rounded-full p-1 shadow-lg">
                <Heart className="h-3 w-3 text-white fill-white" />
              </div>
            )}
          </div>

          {/* Book Details */}
          <div className="flex-1 min-w-0 space-y-2">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-lg line-clamp-1 group-hover:text-amber-600 transition-colors">
                  {book.title}
                </h3>
                {book.series_title && (
                  <p className="text-sm text-amber-600 dark:text-amber-400 line-clamp-1">
                    {book.series_title} {book.volume_number && `Vol. ${book.volume_number}`}
                    {book.volume_title && `: ${book.volume_title}`}
                  </p>
                )}
                <p className="text-sm text-muted-foreground line-clamp-1">
                  by {book.author}
                </p>
              </div>

              {/* Status Badge - Unread, Reading, or Finished */}
              {reading_status === 'finished' ? (
                <Badge className="bg-green-500 text-white shadow-lg flex-shrink-0">
                  Read
                </Badge>
              ) : reading_status === 'reading' ? (
                <Badge className="bg-blue-500 text-white shadow-lg flex-shrink-0">
                  Reading
                </Badge>
              ) : null}
            </div>

            {/* Rating */}
            {rating && (
              <div className="flex items-center gap-2">
                {renderStars(rating)}
                <span className="text-sm text-muted-foreground">
                  {rating.toFixed(1)}
                </span>
              </div>
            )}

            {/* Description */}
            {book.description && (
              <p className="text-sm text-muted-foreground line-clamp-2">
                {book.description}
              </p>
            )}

            {/* Genre and Date */}
            <div className="flex items-center gap-2 flex-wrap">
              {book.genre && (
                <Badge variant="outline" className="text-xs">
                  {book.genre}
                </Badge>
              )}
              {book.date_of_first_publish && (
                <span className="text-xs text-muted-foreground">
                  Published: {new Date(book.date_of_first_publish).getFullYear()}
                </span>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default BookCard;
