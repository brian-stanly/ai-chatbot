import {
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  ElementRef,
  ViewChild,
  AfterViewChecked,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Message } from '../../services/chat.service';
import { MessageBubbleComponent } from '../message-bubble/message-bubble.component';

@Component({
  selector: 'app-chat-window',
  standalone: true,
  imports: [CommonModule, MessageBubbleComponent],
  templateUrl: './chat-window.component.html',
  styleUrl: './chat-window.component.scss',
})
export class ChatWindowComponent implements OnChanges, AfterViewChecked {
  @Input() messages: Message[] = [];
  @Input() isLoading = false;

  @ViewChild('scrollAnchor') private scrollAnchor!: ElementRef;

  private shouldScroll = false;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['messages'] || changes['isLoading']) {
      this.shouldScroll = true;
    }
  }

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  private scrollToBottom(): void {
    try {
      this.scrollAnchor.nativeElement.scrollIntoView({ behavior: 'smooth' });
    } catch {}
  }

  trackByIndex(index: number): number {
    return index;
  }
}
