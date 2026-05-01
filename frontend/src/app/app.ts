import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, Message } from './services/chat.service';
import { ChatWindowComponent } from './components/chat-window/chat-window.component';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatWindowComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  title = 'AI Chatbot';

  messages: Message[] = [];
  userInput = '';
  isLoading = false;
  errorMessage = '';

  constructor(
    private chatService: ChatService,
    private cdr: ChangeDetectorRef
  ) {}

  sendMessage(): void {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    this.userInput = '';
    this.errorMessage = '';
    this.isLoading = true;

    // Optimistically add user message
    this.messages = [...this.messages, { role: 'user', content: text }];

    this.chatService.sendMessage(text, this.getHistoryWithoutLast()).subscribe({
      next: (res) => {
        console.log('Received response:', res);
        this.messages = [
          ...this.messages,
          { role: 'assistant', content: res.response },
        ];
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Chat error:', err);
        this.isLoading = false;
        this.errorMessage =
          err?.error?.detail ?? 'Failed to reach the server. Is the backend running?';
        this.cdr.detectChanges();
      },
    });
  }

  /** Returns history without the optimistically added user message (backend builds it). */
  private getHistoryWithoutLast(): Message[] {
    return this.messages.slice(0, -1);
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  clearChat(): void {
    this.messages = [];
    this.errorMessage = '';
  }
}
