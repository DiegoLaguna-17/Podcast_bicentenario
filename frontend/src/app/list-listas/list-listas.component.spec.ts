import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListListasComponent } from './list-listas.component';

describe('ListListasComponent', () => {
  let component: ListListasComponent;
  let fixture: ComponentFixture<ListListasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListListasComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListListasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
