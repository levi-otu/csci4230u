/**
 * ClubDiscussions Component
 * Displays recent club discussion threads
 */

import React from 'react';
import { MessageCircle, User, Clock } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import { Badge } from '@/global/components/ui/badge';
import { Button } from '@/global/components/ui/button';

export interface Discussion {
  id: string;
  title: string;
  author: {
    id: string;
    username: string;
    avatarUrl?: string;
  };
  createdAt: string;
  lastActivityAt: string;
  replyCount: number;
  excerpt?: string;
  tags?: string[];
  isPinned?: boolean;
}

export interface ClubDiscussionsProps {
  discussions: Discussion[];
  onDiscussionClick?: (discussionId: string) => void;
  onNewDiscussionClick?: () => void;
  isLoading?: boolean;
}

/**
 * ClubDiscussions component
 */
export const ClubDiscussions: React.FC<ClubDiscussionsProps> = ({
  discussions,
  onDiscussionClick,
  onNewDiscussionClick,
  isLoading = false,
}) => {
  // Format relative time
  const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;

    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  // Sort discussions: pinned first, then by last activity
  const sortedDiscussions = [...discussions].sort((a, b) => {
    if (a.isPinned && !b.isPinned) return -1;
    if (!a.isPinned && b.isPinned) return 1;
    return new Date(b.lastActivityAt).getTime() - new Date(a.lastActivityAt).getTime();
  });

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Discussions</CardTitle>
            <CardDescription>
              Recent conversations and topics
            </CardDescription>
          </div>
          {onNewDiscussionClick && (
            <Button onClick={onNewDiscussionClick} size="sm">
              New Discussion
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-center space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
              <p className="text-sm text-muted-foreground">Loading discussions...</p>
            </div>
          </div>
        ) : discussions.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="p-4 bg-muted rounded-full mb-4">
              <MessageCircle className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              No discussions yet. Start the conversation!
            </p>
            {onNewDiscussionClick && (
              <Button onClick={onNewDiscussionClick} variant="outline">
                Create First Discussion
              </Button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {sortedDiscussions.map((discussion) => (
              <div
                key={discussion.id}
                onClick={() => onDiscussionClick?.(discussion.id)}
                className="p-4 border rounded-lg hover:bg-muted/50 transition-colors cursor-pointer"
              >
                {/* Header */}
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      {discussion.isPinned && (
                        <Badge variant="outline" className="text-xs">
                          Pinned
                        </Badge>
                      )}
                      <h4 className="font-semibold text-sm line-clamp-1">
                        {discussion.title}
                      </h4>
                    </div>
                    {discussion.excerpt && (
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {discussion.excerpt}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-1.5 text-muted-foreground">
                    <MessageCircle className="h-3.5 w-3.5" />
                    <span className="text-xs">{discussion.replyCount}</span>
                  </div>
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between gap-3 mt-3">
                  <div className="flex items-center gap-2">
                    {discussion.author.avatarUrl ? (
                      <img
                        src={discussion.author.avatarUrl}
                        alt={discussion.author.username}
                        className="w-5 h-5 rounded-full"
                      />
                    ) : (
                      <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center">
                        <User className="h-3 w-3 text-muted-foreground" />
                      </div>
                    )}
                    <span className="text-xs text-muted-foreground">
                      {discussion.author.username}
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    {discussion.tags && discussion.tags.length > 0 && (
                      <div className="flex gap-1">
                        {discussion.tags.slice(0, 2).map((tag, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    )}
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      <span className="text-xs">
                        {formatRelativeTime(discussion.lastActivityAt)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ClubDiscussions;
