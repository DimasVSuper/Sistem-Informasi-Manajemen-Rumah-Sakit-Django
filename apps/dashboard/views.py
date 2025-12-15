from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.views.decorators.http import require_http_methods
from apps.pasien.models import Pasien
from apps.dokter.models import Dokter
from apps.rekam_medis.models import RekamMedis
from apps.rawat_inap.models import RawatInap
from apps.rawat_jalan.models import RawatJalan
from apps.keuangan.models import Invoice, Pembayaran


@require_http_methods(["GET"])
def landing_page(request):
    """Landing page untuk root URL"""
    return render(request, 'landing.html')