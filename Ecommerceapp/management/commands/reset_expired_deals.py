# your_app/management/commands/reset_expired_deals.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from Ecommerceapp.models import Deal_of_the_day

class Command(BaseCommand):
    help = 'Reset prices of products with expired deals'
    print(f"Current timezone: {timezone.get_current_timezone()}")
    print(f"Current datetime (timezone-aware): {timezone.now()}")


    def handle(self, *args, **options):
        expired_deals = Deal_of_the_day.objects.filter(deal_datetime__lt=timezone.now())
        
        for deal in expired_deals:
            # Reset the product's price to the original price
            deal.product.price = deal.product.original_price
            deal.product.original_price = None
            deal.product.save()

            # Delete the expired deal
            deal.delete()

        self.stdout.write(self.style.SUCCESS('Expired deals reset successfully'))
