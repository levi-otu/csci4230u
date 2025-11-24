/**
 * LibraryStats Component
 * Displays beautiful statistics cards for the user's library
 */

import React, { useState } from 'react';
import { BookOpen, BookCheck, Heart, Star, ListChecks, TrendingUp, Calendar, ChevronDown, ChevronUp } from 'lucide-react';
import { Card, CardContent } from '@/global/components/ui/card';
import type { LibraryStats as LibraryStatsType } from '@/global/models/library.models';

interface LibraryStatsProps {
  stats: LibraryStatsType;
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  subtitle?: string;
  gradient: string;
  onClick?: () => void;
  isClickable?: boolean;
}

const StatCard: React.FC<StatCardProps> = ({ icon, label, value, subtitle, gradient, onClick, isClickable }) => (
  <Card
    className={`overflow-hidden bg-card border-border hover:shadow-lg transition-all duration-300 ${isClickable ? 'cursor-pointer hover:border-amber-500/50' : ''}`}
    onClick={onClick}
  >
    <CardContent className="p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground mb-2">{label}</p>
          <p className="text-3xl font-bold">{value}</p>
          {subtitle && (
            <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`p-3 rounded-xl ${gradient}`}>
          {icon}
        </div>
      </div>
    </CardContent>
  </Card>
);

/**
 * LibraryStats Component
 */
export const LibraryStats: React.FC<LibraryStatsProps> = ({ stats }) => {
  const [showDetailedStats, setShowDetailedStats] = useState(false);
  const {
    total_books,
    read_books,
    unread_books,
    favorite_books,
    total_reading_lists,
    average_rating,
    books_read_this_year,
    books_read_this_month,
  } = stats;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-4 mb-6">
      {/* Total Books */}
      <StatCard
        icon={<BookOpen className="h-6 w-6 text-white" />}
        label="Total Books"
        value={total_books}
        gradient="bg-gradient-to-br from-blue-500 to-blue-600"
      />

      {/* Books Read - Clickable to toggle detailed stats */}
      <StatCard
        icon={
          <div className="relative">
            <BookCheck className="h-6 w-6 text-white" />
            {(books_read_this_year > 0 || books_read_this_month > 0) && (
              <div className="absolute -bottom-1 -right-1">
                {showDetailedStats ? (
                  <ChevronUp className="h-3 w-3 text-white" />
                ) : (
                  <ChevronDown className="h-3 w-3 text-white" />
                )}
              </div>
            )}
          </div>
        }
        label="Books Read"
        value={read_books}
        subtitle={`${unread_books} currently reading${(books_read_this_year > 0 || books_read_this_month > 0) ? ' • Click for details' : ''}`}
        gradient="bg-gradient-to-br from-green-500 to-green-600"
        onClick={() => setShowDetailedStats(!showDetailedStats)}
        isClickable={books_read_this_year > 0 || books_read_this_month > 0}
      />

      {/* Favorites */}
      <StatCard
        icon={<Heart className="h-6 w-6 text-white" />}
        label="Favorites"
        value={favorite_books}
        gradient="bg-gradient-to-br from-red-500 to-red-600"
      />

      {/* Average Rating */}
      <StatCard
        icon={<Star className="h-6 w-6 text-white" />}
        label="Avg Rating"
        value={average_rating ? average_rating.toFixed(1) : 'N/A'}
        subtitle={average_rating ? 'out of 5.0' : 'No ratings yet'}
        gradient="bg-gradient-to-br from-amber-500 to-amber-600"
      />

      {/* Reading Lists (Span 2 columns on mobile, 1 on larger screens) */}
      {total_reading_lists > 0 && (
        <StatCard
          icon={<ListChecks className="h-6 w-6 text-white" />}
          label="Reading Lists"
          value={total_reading_lists}
          gradient="bg-gradient-to-br from-purple-500 to-purple-600"
        />
      )}

      {/* Books This Year - Only show when detailed stats are toggled */}
      {showDetailedStats && books_read_this_year > 0 && (
        <StatCard
          icon={<TrendingUp className="h-6 w-6 text-white" />}
          label="Read This Year"
          value={books_read_this_year}
          gradient="bg-gradient-to-br from-indigo-500 to-indigo-600"
        />
      )}

      {/* Books This Month - Only show when detailed stats are toggled */}
      {showDetailedStats && books_read_this_month > 0 && (
        <StatCard
          icon={<Calendar className="h-6 w-6 text-white" />}
          label="Read This Month"
          value={books_read_this_month}
          gradient="bg-gradient-to-br from-teal-500 to-teal-600"
        />
      )}
    </div>
  );
};

export default LibraryStats;
