/**
 * CurrentBook Component
 * Displays the current book being read by the club
 */

import React from 'react';
import { Book, User, Calendar } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import { Badge } from '@/global/components/ui/badge';

export interface CurrentBookData {
  title: string;
  author: string;
  coverUrl?: string;
  startDate: string;
  endDate?: string;
  progress?: number; // Percentage 0-100
  currentChapter?: string;
  totalChapters?: number;
}

export interface CurrentBookProps {
  book: CurrentBookData | null;
}

/**
 * CurrentBook component
 */
export const CurrentBook: React.FC<CurrentBookProps> = ({ book }) => {
  // Format date to readable string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (!book) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Current Book</CardTitle>
          <CardDescription>
            The club hasn't started reading a book yet
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="p-4 bg-muted rounded-full mb-4">
              <Book className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm text-muted-foreground">
              No book is currently being read
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Current Book</CardTitle>
        <CardDescription>
          What the club is reading right now
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex gap-4">
          {/* Book Cover */}
          <div className="flex-shrink-0">
            {book.coverUrl ? (
              <img
                src={book.coverUrl}
                alt={book.title}
                className="w-24 h-36 object-cover rounded-md border shadow-sm"
              />
            ) : (
              <div className="w-24 h-36 bg-muted rounded-md border flex items-center justify-center">
                <Book className="h-8 w-8 text-muted-foreground" />
              </div>
            )}
          </div>

          {/* Book Details */}
          <div className="flex-1 space-y-3">
            <div>
              <h3 className="text-lg font-semibold mb-1">{book.title}</h3>
              <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <User className="h-3 w-3" />
                <span>{book.author}</span>
              </div>
            </div>

            {/* Reading Schedule */}
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">
                {formatDate(book.startDate)}
                {book.endDate && ` - ${formatDate(book.endDate)}`}
              </span>
            </div>

            {/* Progress */}
            {book.progress !== undefined && (
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Reading Progress</span>
                  <span className="font-medium">{book.progress}%</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary transition-all duration-300"
                    style={{ width: `${book.progress}%` }}
                  />
                </div>
              </div>
            )}

            {/* Chapter Info */}
            {book.currentChapter && (
              <div className="flex gap-2">
                <Badge variant="secondary">
                  Chapter {book.currentChapter}
                  {book.totalChapters && ` of ${book.totalChapters}`}
                </Badge>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CurrentBook;
