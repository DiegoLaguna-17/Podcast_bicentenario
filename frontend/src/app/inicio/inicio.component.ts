import { Component, AfterViewInit, OnDestroy } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-inicio',
  imports: [RouterModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.css']
})
export class InicioComponent implements AfterViewInit, OnDestroy {
  currentSlide = 0;
  private slides: HTMLElement[] = [];
  private indicators: HTMLElement[] = [];
  private totalSlides = 3;
  private intervalId: any;

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.slides = Array.from(document.querySelectorAll('.carousel-item'));
      this.setupIndicators();
      this.showSlide(this.currentSlide);
      this.startAutoRotation();
    }, 0);
  }

  ngOnDestroy(): void {
    this.stopAutoRotation();
  }

  private setupIndicators(): void {
    const indicatorsContainer = document.createElement('div');
    indicatorsContainer.className = 'carousel-indicators';
    
    for (let i = 0; i < this.totalSlides; i++) {
      const indicator = document.createElement('div');
      indicator.className = 'carousel-indicator';
      if (i === this.currentSlide) indicator.classList.add('active');
      indicator.addEventListener('click', () => this.goToSlide(i));
      indicatorsContainer.appendChild(indicator);
    }
    
    document.querySelector('.carousel')?.appendChild(indicatorsContainer);
    this.indicators = Array.from(indicatorsContainer.children) as HTMLElement[];
  }

  private startAutoRotation(): void {
    this.intervalId = setInterval(() => {
      this.nextSlide();
    }, 10000); // 10 segundos
  }

  private stopAutoRotation(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  private goToSlide(index: number): void {
    this.currentSlide = index;
    this.showSlide(this.currentSlide);
    this.resetAutoRotation();
  }

  private resetAutoRotation(): void {
    this.stopAutoRotation();
    this.startAutoRotation();
  }

  private showSlide(index: number): void {
    this.slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });
    
    this.indicators?.forEach((indicator, i) => {
      indicator.classList.toggle('active', i === index);
    });
    
    const inner = document.querySelector('.carousel-inner') as HTMLElement;
    if (inner) {
      inner.style.transform = `translateX(-${index * 100}%)`;
    }
  }

  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
    this.showSlide(this.currentSlide);
    this.resetAutoRotation();
  }

  prevSlide(): void {
    this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
    this.showSlide(this.currentSlide);
    this.resetAutoRotation();
  }
}