from home.models import StudentRecord
from home.utils import render_to_pdf


def ResultList(request):
    template_name = "pdf.html"
    records = StudentRecord.objects.all().order_by("roll_no")

    return render_to_pdf(
        template_name,
        {
            "record": records,
        },
    )